from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.methods import send_media_group
from middlewares import MediaGroupMiddleware
from aiogram.types import Message, InputMediaPhoto
from states import AddNewsStates
from typing import List
from data.db_session import create_session
from data.users import User

router = Router()
router.message.middleware(MediaGroupMiddleware())

@router.message(F.text == "Отмена")  # сработает при любом состоянии добавления новости
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Добавление новости отменено", reply_markup=keyboards.ReplyKeyboardRemove())
    await message.answer(strings.ADMIN_MENU_CAPTION, reply_markup=keyboards.admin_menu_keyboard())

@router.message(F.text, AddNewsStates.heading)
async def heading(message: Message, state: FSMContext):
    await state.update_data(heading=message.text)
    await state.set_state(AddNewsStates.add_images)
    await message.answer("отправьте приложения к новости или любое сообщение")
    
@router.message(AddNewsStates.add_images)
async def add_images(message: Message, state: FSMContext, album: List[Message] = None, bot: Bot = None):
    photos = []
    if album is None:  # если фотографии не были присланы группой
        album = [message]
    for element in album:  # получаем фотографии из всех элементов альбома
        if element.photo:
            photos.append(InputMediaPhoto(media=element.photo[-1].file_id))
    if len(photos) > 10:  # можно прислать не более 10 фотографий, лишние удаляются
        photos = photos[:10]
    await state.update_data({"photos": photos})
    
    with create_session() as session:
        ids = session.query(User).all()
        for id_ in ids:
            await bot.send_media_group(chat_id=id_.id, media=photos)
            data = await state.get_data()
            await bot.send_message(chat_id=id_.id, text=data["heading"])
            try:
                pass
            except:
                print(f"не удалось отправить новость для id={id_.id}")
    await message.answer("Новость опубликована")
