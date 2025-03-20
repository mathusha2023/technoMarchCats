from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.formatting import Pre, Text, Underline
from aiogram.fsm.context import FSMContext
from keyboards import faq_keyboard, cancel_keyboard, moderator_answer_keyboard
from states import UserStates
from data import db_session
from data.questions import Question
from data.message_id import MessageId
from data.moderators import Moderator
from data.comments_and_suggestions import Suggestion
from utils import format_default_questions, format_with_author
import config

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    await message.answer(config.GREETING, reply_markup=faq_keyboard())


@router.message(F.text == "🚫 Отмена")
async def cancel(message: Message, state: FSMContext):
    await message.delete()
    await message.answer("Выберите один из пунктов ниже:", reply_markup=faq_keyboard())
    await state.clear()


@router.message(F.text, UserStates.asking_question)
async def get_question(message: Message, state: FSMContext, bot: Bot):
    session = db_session.create_session()
    try:
        moderator = min(session.query(Moderator).all(), key=lambda m: len(m.questions))
    except ValueError:
        await message.answer("К сожалению, сейчас модераторы отсутствуют. Пожалуйста, попробуйте позже",
                             reply_markup=faq_keyboard())
        await state.clear()
        return
    question = Question(text=message.text, sender=message.from_user.id, moderator=moderator.id,
                        sender_name=message.from_user.first_name)
    session.add(question)
    session.commit()
    msg = await bot.send_message(moderator.user_id,
                                 **format_with_author(message.from_user.first_name, message.text),
                                 reply_markup=moderator_answer_keyboard(question.id))
    message_id = MessageId(message_id=msg.message_id, question=question.id)
    session.add(message_id)
    session.commit()
    await message.answer(
        **Text(
            f"Ваш вопрос добавлен в очередь к модератору ", Underline(moderator.name),
            f" под номером {len(moderator.questions)} и выглядит так:\n",
            Pre(message.text),
            f"\nКак только ответ будет получен, вы сможете увидеть его здесь.").as_kwargs(),
        reply_markup=faq_keyboard())
    await state.clear()


@router.message(F.text, UserStates.voting)
async def get_suggestion(message: Message, state: FSMContext, bot: Bot):
    session = db_session.create_session()
    s = Suggestion(text=message.text, sender=message.from_user.id, sender_name=message.from_user.first_name)
    session.add(s)
    session.commit()
    await state.clear()
    await bot.send_message(config.ADMIN_ID, f"Добавлен новый отзыв! Текущее количество: {s.id}")
    await message.answer("Огромное спасибо за ваш отзыв. Мы будем стараться совершенствоваться ради вас!",
                         reply_markup=faq_keyboard())


@router.message(F.text == "📖 Часто задаваемые вопросы")
async def default_questions(message: Message):
    await message.answer(format_default_questions(), reply_markup=faq_keyboard())


@router.message(F.text == "📩 Задать вопрос")
async def ask_question(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, введите свой вопрос. Модератор постарается ответить на него как можно быстрее.",
                         reply_markup=cancel_keyboard())
    await state.set_state(UserStates.asking_question)


@router.message(F.text == "💡 Поделиться впечатлениями с нами")
async def vote(message: Message, state: FSMContext):
    await message.answer(
        "Пожалуйста, расскажите о вашем впечатлении от нашего бота. Что понравилось, что не очень,"
        " а что было бы неплохо добавить. Ваш отзыв очень важен для нас, ведь вы с каждым днем делаете нас лучше:)",
        reply_markup=cancel_keyboard())
    await state.set_state(UserStates.voting)
