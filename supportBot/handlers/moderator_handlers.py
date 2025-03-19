from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.utils.formatting import Pre, Text, Underline
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from data import db_session
from data.moderators import Moderator
from data.questions import Question
from data.message_id import MessageId
from data.uncommited_moderators import UncommitedModerator
from filters import ModeratorFilter, UncommitedModeratorFilter
from states import ModeratorStates
from keyboards import cancel_keyboard, moderator_answer_keyboard, all_questions_keyboard
from utils import format_with_author

router = Router()


@router.message(Command("start"), UncommitedModeratorFilter())
async def start(message: Message):
    session = db_session.create_session()
    u_m = session.query(UncommitedModerator).filter(UncommitedModerator.user_id == int(message.from_user.id)).first()
    moder = Moderator(user_id=u_m.user_id, name=message.from_user.first_name)
    session.delete(u_m)
    session.add(moder)
    session.commit()
    await message.answer(
        "Здравствуйте! Вы были назначены модератором приюта. Вы можете отвечать на вопросы пользователей.",
        reply_markup=all_questions_keyboard())


@router.message(Command("start"), ModeratorFilter())
async def start(message: Message):
    session = db_session.create_session()
    m = session.query(Moderator).filter(Moderator.user_id == int(message.from_user.id)).first()
    m.name = message.from_user.first_name
    session.commit()
    await message.answer(
        "Здравствуйте! Вы были назначены модератором приюта. Вы можете отвечать на вопросы пользователей.",
        reply_markup=all_questions_keyboard())


@router.message(F.text == "Отмена", ModeratorFilter())
async def add_moderator_cancel(message: Message, state: FSMContext, bot: Bot):
    msg_id: int | None = (await state.get_data()).get("msg_id", None)
    if msg_id is not None:
        await bot.delete_message(message.from_user.id, msg_id)
    await message.delete()
    await state.clear()
    await message.answer("Будьте готовы отвечать на вопросы людей, интересующихся приютом!",
                         reply_markup=all_questions_keyboard())


@router.message(F.text == "Показать все вопросы", ModeratorFilter())
async def add_moderator_cancel(message: Message):
    session = db_session.create_session()
    questions: [Question] = session.query(Moderator).filter(Moderator.user_id == message.from_user.id).first().questions
    if questions:
        for q in questions:
            msg = await message.answer(**format_with_author(q.sender_name, q.text),
                                       reply_markup=moderator_answer_keyboard(q.id))
            message_id = MessageId(message_id=msg.message_id, question=q.id)
            session.add(message_id)
            session.commit()
    else:
        await message.answer("В настоящий момент у гостей приюта нет к вам вопросов",
                             reply_markup=all_questions_keyboard())


@router.callback_query(ModeratorFilter())
async def answer_callback_handler(callback: CallbackQuery, state: FSMContext):
    num = int(callback.data)
    question = db_session.create_session().query(Question).get(num)
    if question is not None:
        await state.set_state(ModeratorStates.answering_question)
        await state.update_data(question_id=num)
        msg = await callback.message.answer(**Text("Введите ответ на вопрос:\n", Pre(question.text)).as_kwargs(),
                                            reply_markup=cancel_keyboard())
        await callback.answer()
        await state.update_data(msg_id=msg.message_id)
    else:
        await callback.answer("Вы уже ответили на этот вопрос!")


@router.message(F.text, ModeratorFilter(), ModeratorStates.answering_question)
async def answer_question(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    session = db_session.create_session()
    question: Question = session.query(Question).get(data["question_id"])
    moderator = session.query(Moderator).get(question.moderator)
    await bot.send_message(question.sender,
                           **Text(f"Получен ответ на ваш вопрос от модератора ", Underline(moderator.name),
                                  "\n",
                                  Pre(question.text),
                                  f"Он выглядит так:\n", Pre(message.text)).as_kwargs())
    await message.answer(f"Ваш ответ на вопрос номер {question.id} успешно отправлен!",
                         reply_markup=all_questions_keyboard())
    for m in question.message_ids:
        await bot.edit_message_text(chat_id=message.from_user.id, message_id=m.message_id,
                                    **format_with_author(question.sender_name, question.text, crossed=True),
                                    reply_markup=moderator_answer_keyboard(question.id))
        session.delete(m)
    session.delete(question)
    session.commit()
    await state.clear()
