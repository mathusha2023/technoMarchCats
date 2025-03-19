from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import desc
from data import db_session
import keyboards
import strings
from data.animal_requests import AnimalRequest
from filters import StatesGroupFilter
from states import GuardianshipListAdminStates
from utils.generate_guardianship_request_message import generate_guardianship_request_message

router = Router()


@router.message(F.text == "📂 В меню",
                StatesGroupFilter(GuardianshipListAdminStates))  # сработает при любом состоянии обновления животного
async def in_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Возвращаю в меню", reply_markup=keyboards.ReplyKeyboardRemove())
    await message.answer(strings.ADMIN_MENU_CAPTION, reply_markup=keyboards.admin_menu_keyboard())


@router.message(F.text == "↘️ Следующая",
                GuardianshipListAdminStates.watching)
async def next_request(message: Message, state: FSMContext):
    data = await state.get_data()
    last_request_id = data["last_request_id"]

    session = db_session.create_session()
    animal_request = session.query(AnimalRequest).where(AnimalRequest.id < last_request_id).order_by(
        desc(AnimalRequest.id)).first()
    if animal_request is None:  # возможно мы дошли до самой последней заявки, надо начать поиск сначала
        animal_request = session.query(AnimalRequest).order_by(desc(AnimalRequest.id)).first()
    if animal_request is None:  # если и в этот раз заявок не найдено, то их просто нет
        return await message.answer("В настоящий момент все заявки рассмотрены")
    await state.update_data({"last_request_id": animal_request.id})
    await generate_guardianship_request_message(animal_request, message)
