from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

import strings
from filters import StatesGroupFilter
from states import TestStates
import keyboards
from aiogram import Router, F, Bot
from sqlalchemy import and_

from data.animal_requests import AnimalRequest
from data import db_session
from data.users import User
from data.animals import Animal
from utils.send_message_to_all_administrators import send_message_to_all_administrators

router = Router()


@router.callback_query(F.data == "test")
async def test_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("""<b>1. Какой у вас образ жизни?</b>
    <b>1️⃣</b> Спокойный, люблю проводить время дома.
    <b>2️⃣</b> Активный ️, часто гуляю или занимаюсь спортом.
    <b>3️⃣</b> Занимаюсь работой или учебой, но люблю проводить время с животными.""",
                                  reply_markup=keyboards.test_reply_keyboard())
    await state.set_state(TestStates.question1)
    await state.update_data({"1️⃣": 0, "2️⃣": 0, "3️⃣": 0})
    await callback.answer()


@router.message(F.text == "📂 В меню", TestStates.result, StatesGroupFilter(TestStates))
async def take(message: Message, state: FSMContext):
    await message.answer("Возвращаю в меню", reply_markup=keyboards.ReplyKeyboardRemove())
    await message.answer(strings.GREETING, reply_markup=keyboards.start_keyboard())
    await state.clear()


@router.message(F.text == "📥 Хочу взять!", TestStates.result, StatesGroupFilter(TestStates))
async def take_cat(message: Message, state: FSMContext, bot: Bot):
    session = db_session.create_session()
    animal_id = (await state.get_data())["animal_id"]

    user = session.query(User).where(User.id == message.from_user.id).first()
    animal = session.query(Animal).where(Animal.id == animal_id).first()
    if animal is None:  # не смогли найти животное, значит животных просто нет
        return await message.answer("Сейчас вы не можете взять животное!")

    last_request = session.query(AnimalRequest).where(and_(AnimalRequest.userId == user.id,
                                                           AnimalRequest.animalId == animal.id)).first()  # ищем заявку от пользователя на это животное в базе данных
    if last_request:  # если такой запрос уже существует, то заново подавать запрос не будем
        await message.answer(
            "Заявка на этого котика ужа была подана и ожидает рассмотрения администратором. Пожалуйста, дождитесь обратной связи!",
            reply_markup=keyboards.ReplyKeyboardRemove())
    else:
        animal_request = AnimalRequest()
        animal_request.user = user
        animal_request.animal = animal
        session.add(animal_request)
        session.commit()

        await send_message_to_all_administrators(bot,
                                                 "Подана новая заявка!")  # оповещаем всех администраторов о подаче заявки

        await message.answer("Ваша заявка отправлена! Администратор свяжется с вами в ближайшее время",
                             reply_markup=keyboards.ReplyKeyboardRemove())
    await message.answer(strings.GREETING, reply_markup=keyboards.start_keyboard())
    await state.clear()
