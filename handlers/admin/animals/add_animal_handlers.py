from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from datetime import date, datetime
import config
from data.users import User
import strings
import keyboards
from middlewares import MediaGroupMiddleware
from states import AddAnimalStates
from utils.add_animal_to_db import add_animal_to_db

router = Router()
router.message.middleware(MediaGroupMiddleware())


@router.message(F.text, AddAnimalStates.naming)
async def naming(message: Message, state: FSMContext):
    await state.update_data({"name": message.text})
    await state.set_state(AddAnimalStates.adding_gender)
    await message.answer("Замечательно! Наш новый друг мальчик или девочка? Выбери: 1 - мальчик, 2 - девочка", reply_markup=keyboards.select_animal_gender_keyboard())


@router.message(F.text.in_(["1", "2"]), AddAnimalStates.adding_gender)
async def adding_gender(message: Message, state: FSMContext):
    await state.update_data({"gender": int(message.text) - 1})
    await state.set_state(AddAnimalStates.adding_birthday)
    await message.answer("Отлично! Когда у нашего нового питомца день рождения? Введите дату в формате dd.mm.yyyy", reply_markup=keyboards.ReplyKeyboardRemove())


@router.message(F.text, AddAnimalStates.adding_gender)
async def adding_gender(message: Message):
    await message.answer("Пришли 1, если у нас мальчик, и 2 - если девочка!")


@router.message(F.text, AddAnimalStates.adding_birthday)
async def adding_age(message: Message, state: FSMContext):
    try:
        date_ = datetime.strptime(message.text, "%d.%m.%Y").date()
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


# TODO: сделать обработку одиночных фотографий
@router.message(AddAnimalStates.adding_images)
async def adding_images(message: Message, state: FSMContext, album: [Message]):
    photos = []
    for element in album:
        if element.photo:
            photos.append(element.photo[-1].file_id)
    await state.update_data({"photos": photos})
    await state.set_state(AddAnimalStates.adding_images)
    await message.answer("Замечательно! Вот как выглядит карточка этого пушистого комочка счастья:")
    add_animal_to_db(await state.get_data())
