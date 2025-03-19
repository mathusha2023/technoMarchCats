from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from datetime import datetime
from data import db_session
import keyboards
import strings
from data.animals_tags import AnimalTag
from filters import StatesGroupFilter
from middlewares import MediaGroupMiddleware
from states import AddAnimalStates
from utils.add_animal_to_db import add_animal_to_db
from utils.generate_animal_card_by_state import generate_animal_card_by_state

router = Router()
router.message.middleware(MediaGroupMiddleware())

@router.message(F.text == "🚫 Отмена", StatesGroupFilter(AddAnimalStates))  # сработает при любом состоянии добавления животного
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Добавление котика отменено", reply_markup=keyboards.ReplyKeyboardRemove())
    await message.answer(strings.ADMIN_MENU_CAPTION, reply_markup=keyboards.admin_menu_keyboard())


@router.message(F.text, AddAnimalStates.naming)
async def naming(message: Message, state: FSMContext):
    await state.update_data({"name": message.text})
    await state.set_state(AddAnimalStates.adding_gender)
    await message.answer("Замечательно! Наш новый друг мальчик или девочка? Выберите: 1 - мальчик, 2 - девочка",
                         reply_markup=keyboards.select_animal_gender_keyboard())


@router.message(F.text.in_(["1", "2"]), AddAnimalStates.adding_gender)
async def adding_gender(message: Message, state: FSMContext):
    await state.update_data({"gender": int(message.text) - 1})
    await state.set_state(AddAnimalStates.adding_birthday)
    await message.answer("Отлично! Когда у нашего нового питомца день рождения? Введите дату в формате dd.mm.yyyy",
                         reply_markup=keyboards.cancel_keyboard())


@router.message(F.text, AddAnimalStates.adding_gender)
async def adding_gender(message: Message):
    await message.answer("Пришлите 1, если у нас мальчик, и 2 - если девочка!")


@router.message(F.text, AddAnimalStates.adding_birthday)
async def adding_age(message: Message, state: FSMContext):
    try:
        date_ = datetime.strptime(message.text, "%d.%m.%Y").date()
        if date_ > datetime.today().date():
            return await message.answer("Введите корректную дату рождения!")
        await state.update_data({"birthday": date_})
        await state.set_state(AddAnimalStates.describing)
        await message.answer("Великолепно! Опишите котика")
    except ValueError:
        await message.answer("Введите дату рождения в требуемом формате!")


@router.message(F.text, AddAnimalStates.describing)
async def describing(message: Message, state: FSMContext):
    await state.update_data({"description": message.text})
    await state.set_state(AddAnimalStates.adding_images)
    await message.answer("Записано! Теперь добавим картинки нашего питомца. Пришлите до 10 фотографий котика")


@router.message(AddAnimalStates.adding_images)
async def adding_images(message: Message, state: FSMContext, album: [Message] = None):
    photos = []
    if album is None:  # если фотографии не были присланы группой
        album = [message]
    for element in album:  # получаем фотографии из всех элементов альбома
        if element.photo:
            photos.append(element.photo[-1].file_id)
    if len(photos) > 10:  # можно прислать не более 10 фотографий, лишние удаляются
        photos = photos[:10]
    if not photos:
        return await message.answer("Пришлите от одной до десяти фотографий котика!")

    await state.update_data({"photos": photos})
    await state.set_state(AddAnimalStates.adding_tags)
    await message.answer(
        "Замечательно! Последний пункт: выберите теги, которые будут у нашего любимца. Пришлите номера выбранных из списка ниже тегов через пробел. Например, 1 2 3 8")
    session = db_session.create_session()
    tags = session.query(AnimalTag).order_by(AnimalTag.id).all()
    s = ""
    for tag in tags:
        s += f"{tag.id} - {tag.tag}\n"
    await message.answer(s)


@router.message(F.text, AddAnimalStates.adding_tags)
async def adding_tags(message: Message, state: FSMContext):
    try:
        tags = []
        session = db_session.create_session()
        indexes = map(int, message.text.split())
        for i in indexes:
            tag = session.query(AnimalTag).where(AnimalTag.id == i).first()
            if tag is None:
                raise ValueError
            tags.append(tag)
        await state.update_data({"tags": tags, "db_session": session})
        await message.answer("Замечательно! Вот как выглядит карточка этого пушистого комочка счастья:")
        await generate_animal_card_by_state(await state.get_data(), message)  # отправляем получившуюся карточку животного
        await message.answer("Всё верно?", reply_markup=keyboards.accept_adding_animal_keyboard())
        await state.set_state(AddAnimalStates.confirm_adding)
    except ValueError:
        await message.answer("Пришлите корректные номера тегов!")


@router.message(F.text == "✅ Да, все так", AddAnimalStates.confirm_adding)
async def accept_adding(message: Message, state: FSMContext):
    await add_animal_to_db(await state.get_data())
    await message.answer("Наш новый питомец успешно добавлен в базу данных!", reply_markup=keyboards.ReplyKeyboardRemove())
    await state.clear()
    await message.answer(strings.ADMIN_MENU_CAPTION, reply_markup=keyboards.admin_menu_keyboard())


@router.message(F.text == "✏️ Заполнить карточку заново", AddAnimalStates.confirm_adding)
async def restart_adding(message: Message, state: FSMContext):
    await state.set_data({})  # очищаем все полученные данные
    await state.set_state(AddAnimalStates.naming)  # заново переходим к выбору имени питомца
    await message.answer("Введите имя нашего котика", reply_markup=keyboards.ReplyKeyboardRemove())
