import logging
from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder

from config import BANNED_USERS
from filters import StatesGroupFilter
from middlewares import MediaGroupMiddleware
from aiogram.types import Message
from states import AddVolunteerNewsStates
from typing import List
from data.db_session import create_session
from data.users import User
import keyboards
import strings

router = Router()
router.message.middleware(MediaGroupMiddleware())


@router.message(F.text == "🚫 Отмена",
                StatesGroupFilter(AddVolunteerNewsStates))  # сработает при любом состоянии добавления новости
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Добавление новости отменено", reply_markup=keyboards.ReplyKeyboardRemove())
    await message.answer(strings.ADMIN_MENU_CAPTION, reply_markup=keyboards.admin_menu_keyboard())


@router.message(F.text, AddVolunteerNewsStates.heading)
async def heading(message: Message, state: FSMContext):
    await state.update_data(heading=message.text)
    await state.set_state(AddVolunteerNewsStates.add_images)
    await message.answer("Отправьте приложения к новости (до 10 фотографий)")


@router.message(AddVolunteerNewsStates.add_images)
async def add_images(message: Message, state: FSMContext, album: List[Message] = None, bot: Bot = None):
    photos = []
    if album is None:  # если фотографии не были присланы группой
        album = [message]
    for element in album:  # получаем фотографии из всех элементов альбома
        if element.photo:
            photos.append(element.photo[-1].file_id)

    if not photos:  # если не было прислано ни одной фотографии
        return await message.answer("Пришлите от одной до десяти фотографии для приложения!")
    if len(photos) > 10:  # можно прислать не более 10 фотографий, лишние удаляются
        photos = photos[:10]

    with create_session() as session:
        data = await state.get_data()

        # компонуем новость для отправки
        album_builder = MediaGroupBuilder(
            caption=data["heading"]
        )
        for photo in photos:
            album_builder.add_photo(photo)
        media_group = album_builder.build()

        users = session.query(User).where(
            User.id != message.from_user.id, User.isVolunteer==True).all()  # получаем всех волонтеров кроме отправителя новости
        for user in users:
            if user.id in BANNED_USERS:  # заблокированным пользователям новости не нужны
                continue
            try:
                await bot.send_media_group(chat_id=user.id,
                                           media=media_group)  # отправляем новость каждому пользователю
            except TelegramBadRequest:
                logging.info(f"Пользователя {user.id} не существует!")

    await message.answer("Новость опубликована!")
    await state.clear()
    await message.answer(strings.ADMIN_MENU_CAPTION, reply_markup=keyboards.admin_menu_keyboard())
