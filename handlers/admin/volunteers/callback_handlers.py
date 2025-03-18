from states import AddVolunteerNewsStates
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from data import db_session
import strings
import keyboards
from data.users import User
from utils.generate_user_info_message import generate_user_info_message

router = Router()


@router.callback_query(F.data == "admin_menu")
async def back_callback(callback: CallbackQuery):
    await callback.message.edit_text(strings.ADMIN_MENU_CAPTION, reply_markup=keyboards.admin_menu_keyboard())


@router.callback_query(F.data == "volunteers_interaction")
async def volunteers_interaction_callback(callback: CallbackQuery):
    await callback.message.edit_text("Волонтёры - наши главные друзья! Вот как вы можете взаимодействовать с ними:", reply_markup=keyboards.admin_volunteer_interaction_keyboard())
    await callback.answer()


@router.callback_query(F.data == "volunteer_news")
async def post_news_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddVolunteerNewsStates.heading)
    await callback.message.answer("Введите заголовок обращения", reply_markup=keyboards.cancel_keyboard())
    await callback.answer()


@router.callback_query(F.data == "volunteer_list")  # отображаем первую страницу списка волонтеров
async def watch_users_callback(callback: CallbackQuery):
    session = db_session.create_session()
    users = session.query(User).where(User.isVolunteer).limit(4).all()
    users_count = session.query(User).where(User.isVolunteer).count()

    await callback.message.edit_text(strings.VOLUNTEER_LIST_CAPTION,
                                     reply_markup=keyboards.volunteers_list_keyboard(users, 1, show_right=users_count > 4))


@router.callback_query(F.data.startswith("volunteer_control_right_"))  # перелистывание списка пользователей вправо по кнопке
async def user_control_right_callback(callback: CallbackQuery):
    fourth_number = int(
        callback.data.split("_")[-1])  # получаем номер последней четверки, в которой находился пользователь
    session = db_session.create_session()
    users = session.query(User).where(User.isVolunteer).offset(fourth_number * 4).limit(4).all()
    users_count = session.query(User).where(User.isVolunteer).count()
    await callback.message.edit_reply_markup(
        reply_markup=keyboards.volunteers_list_keyboard(users, fourth_number + 1, show_left=True,
                                                   show_right=users_count > (fourth_number + 1) * 4))
    await callback.answer()


@router.callback_query(F.data.startswith("volunteer_control_left_"))  # перелистывание списка пользователей влево по кнопке
async def user_control_left_callback(callback: CallbackQuery):
    fourth_number = int(
        callback.data.split("_")[-1])  # получаем номер последней четверки, в которой находился пользователь
    session = db_session.create_session()
    users = session.query(User).where(User.isVolunteer).offset((fourth_number - 2 if fourth_number > 1 else 0) * 4).limit(4).all()
    await callback.message.edit_reply_markup(
        reply_markup=keyboards.volunteers_list_keyboard(users, fourth_number - 1, show_right=True,
                                                   show_left=fourth_number > 2))
    await callback.answer()


@router.callback_query(F.data.startswith("volunteer_control_"))  # выбор администратором пользователя совершен
async def user_control(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.data.split("_")[-1])  # получаем telegram user_id выбранного пользователя
    session = db_session.create_session()
    user = session.query(User).where(User.id == user_id).first()
    if user.id == callback.from_user.id:
        return await callback.answer("Это вы!")
    await generate_user_info_message(user, callback.message)
    await state.update_data(user=user, session=session)
    await callback.answer()


# @router.callback_query(F.data.startswith("cancel_user_controlling"))
# async def ban_user_callback(callback: CallbackQuery, state: FSMContext):
#     await state.clear()
#     await callback.message.delete()
