from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

import strings
from states import AddVolunteerNewsStates
import keyboards
from aiogram import Router, F

router = Router()


@router.callback_query(F.data == "admin_menu")
async def back_callback(callback: CallbackQuery):
    await callback.message.edit_text(strings.ADMIN_MENU_CAPTION, reply_markup=keyboards.admin_menu_keyboard())


@router.callback_query(F.data == "volunteers_interaction")
async def volunteers_interaction_callback(callback: CallbackQuery):
    await callback.message.edit_text("Список действий с волонтёрами", reply_markup=keyboards.admin_volunteer_interaction_keyboard())
    await callback.answer()


@router.callback_query(F.data == "volunteer_news")
async def post_news_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddVolunteerNewsStates.heading)
    await callback.message.answer("Введите заголовок новости", reply_markup=keyboards.cancel_keyboard())
    await callback.answer()