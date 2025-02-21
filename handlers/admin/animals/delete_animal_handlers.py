from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from data import db_session
import keyboards
from data.animals import Animal
from middlewares import MediaGroupMiddleware
from states import DeleteAnimalStates

router = Router()
router.message.middleware(MediaGroupMiddleware())


@router.message(F.text.isdigit(), DeleteAnimalStates.index_input)
async def delete_animal(message: Message, state: FSMContext):
    animal_id = int(message.text)
    session = db_session.create_session()
    animal = session.query(Animal).where(Animal.id == animal_id).first()
    if animal is None:
        return await message.answer(f"Животного с ID {animal_id} не существует! Введите существующий ID", reply_markup=message.reply_markup)
    await state.set_state(DeleteAnimalStates.confirm_delete)
    await state.update_data({"session": session, "animal": animal})
    await message.answer(f"Вы уверены, что хотите удалить {animal.name} с ID {animal.id} из базы данных?", reply_markup=keyboards.yes_or_no_keyboard())


@router.message(DeleteAnimalStates.index_input)
async def delete_animal(message: Message):
    await message.answer("Введите корректный ID животного!")


@router.message(F.text == "Да", DeleteAnimalStates.confirm_delete)
async def delete_animal(message: Message, state: FSMContext):
    data = await state.get_data()
    session = data["session"]
    animal = data["animal"]
    session.delete(animal)
    session.commit()

    await state.set_state(DeleteAnimalStates.index_input)
    await state.set_data({})
    await message.answer("Успешно удалено!", reply_markup=keyboards.ReplyKeyboardRemove())
    await message.answer("Введите ID животного, которое хотите удалить", reply_markup=keyboards.watch_animals_ids_keyboard())


@router.message(F.text == "Нет", DeleteAnimalStates.confirm_delete)
async def delete_animal(message: Message, state: FSMContext):
    await state.set_state(DeleteAnimalStates.index_input)
    await state.set_data({})
    await message.answer("Введите ID животного, которое хотите удалить", reply_markup=keyboards.ReplyKeyboardRemove())


@router.message(F.text == "В меню", DeleteAnimalStates.confirm_delete)
async def delete_animal(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Возврат в меню выбора действия", reply_markup=keyboards.ReplyKeyboardRemove())
    await message.answer("Вот список возможных действий:", reply_markup=keyboards.admin_animals_keyboard())
