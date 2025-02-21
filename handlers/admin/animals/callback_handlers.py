from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy import desc
from data import db_session
import strings
import keyboards
from data.animal_requests import AnimalRequest
from states import AddAnimalStates, DeleteAnimalStates, UpdateAnimalStates, GuardianshipListAdminStates
from utils.generate_animals_admin_list import generate_animals_admin_list
from utils.generate_guardianship_request_message import generate_guardianship_request_message

router = Router()


@router.callback_query(F.data == "escape_to_admin_menu")
async def escape_to_admin_menu_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await animals_list_callback(callback)


@router.callback_query(F.data == "close_animals_admin_list")
async def close_animals_admin_list_callback(callback: CallbackQuery):
    await callback.message.delete()


@router.callback_query(F.data == "animals")
async def animals_list_callback(callback: CallbackQuery):
    await callback.message.edit_text("Вот список возможных действий:", reply_markup=keyboards.admin_animals_keyboard())


@router.callback_query(F.data == "admin_menu")
async def back_callback(callback: CallbackQuery):
    await callback.message.edit_text(strings.ADMIN_MENU_CAPTION, reply_markup=keyboards.admin_menu_keyboard())


@router.callback_query(F.data == "add_animal")
async def add_animal_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddAnimalStates.naming)
    await callback.message.answer("Как зовут нашего нового котика?", reply_markup=keyboards.cancel_keyboard())
    await callback.answer()


@router.callback_query(F.data == "delete_animal")
async def delete_animal_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(DeleteAnimalStates.index_input)
    await callback.message.edit_text("Введите ID животного, которое хотите удалить", reply_markup=keyboards.watch_animals_ids_keyboard())
    await callback.answer()


@router.callback_query(F.data == "update_animal")
async def update_animal_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UpdateAnimalStates.index_input)
    await callback.message.edit_text("Введите ID животного, информацию о котором вы хотите обновить", reply_markup=keyboards.watch_animals_ids_keyboard())
    await callback.answer()


@router.callback_query(F.data == "animals_admin_list")
async def animals_admin_list_callback(callback: CallbackQuery):
    await generate_animals_admin_list(callback.message)
    await callback.answer()


@router.callback_query(F.data == "guardianship_list")
async def guardianship_list_callback(callback: CallbackQuery, state: FSMContext):
    session = db_session.create_session()
    animal_request = session.query(AnimalRequest).order_by(desc(AnimalRequest.id)).first()
    await state.set_state(GuardianshipListAdminStates.watching)
    if animal_request is None:
        await callback.answer()
        return await callback.message.answer("В настоящий момент все заявки рассмотрены")

    await state.update_data({"last_request_id": animal_request.id})
    await callback.message.answer("Вот все заявки от пользователей:", reply_markup=keyboards.watch_guardianship_keyboard())
    await generate_guardianship_request_message(animal_request, callback.message)
    await callback.answer()


@router.callback_query(F.data.startswith("delete_request_"))
async def delete_request_callback(callback: CallbackQuery):
    request_id = int(callback.data.split("_")[-1])  # получаем ID заявки
    session = db_session.create_session()
    animal_request = session.query(AnimalRequest).where(AnimalRequest.id == request_id).first()
    if animal_request:
        session.delete(animal_request)
        session.commit()
    await callback.message.delete()
    await callback.answer("Заявка успешно удалена")
