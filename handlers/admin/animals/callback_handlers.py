from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
import strings
import keyboards
from states import AddAnimalStates, DeleteAnimalStates
from utils.generate_animals_admin_list import generate_animals_admin_list

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


@router.callback_query(F.data == "animals_admin_list")
async def animals_admin_list_callback(callback: CallbackQuery):
    await generate_animals_admin_list(callback.message)
    await callback.answer()
