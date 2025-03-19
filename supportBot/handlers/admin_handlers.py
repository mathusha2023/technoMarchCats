from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from filters import AdminFilter
from states import AdminStates
from keyboards import (admin_keyboard, cancel_keyboard, change_default_questions_keyboard, all_questions_keyboard,
                       delete_moderator_keyboard, faq_keyboard, moderator_answer_keyboard)
from data import db_session
from data.moderators import Moderator
from data.uncommited_moderators import UncommitedModerator
from data.comments_and_suggestions import Suggestion
from data.message_id import MessageId
from utils import format_default_questions, format_with_author, format_moderators
import config

router = Router()
router.message.filter(AdminFilter())


@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Приветствую! Я помогу вам в организации обратной связи с посетителями приюта. Сейчас вы можете добавить модераторов, "
                         "которые будут отвечать на вопросы, задаваемые пользователями, изменить приветствие "
                         "людей или настроить вопросы по умолчанию и ответы на них.",
                         reply_markup=admin_keyboard())


@router.message(F.text == "Отмена")
async def add_moderator_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.delete()
    await message.answer("Выберите одно из действий ниже!", reply_markup=admin_keyboard())


@router.message(F.text, AdminStates.adding_moderator)
async def add_moderator(message: Message, state: FSMContext, bot: Bot):
    if message.text.isdigit():
        id_ = int(message.text)
        session = db_session.create_session()
        u_m = session.query(UncommitedModerator).filter(UncommitedModerator.user_id == id_).first()
        m = session.query(Moderator).filter(Moderator.user_id == id_).first()
        if u_m or m:
            await message.answer(
                f"Модератор с user id [{id_}] уже был добавлен!",
                reply_markup=admin_keyboard())
        else:
            try:
                await bot.send_message(id_,
                                       "Здравствуйте! Вы были назначены модератором приюта и можете отвечать на"
                                       " вопросы пользователей. Пожалуйста, используйте команду [/start], чтобы бот мог"
                                       " запомнить ваше имя.",
                                       reply_markup=all_questions_keyboard())
                new_moder = Moderator(user_id=id_)
                await message.answer(
                    "Модератор успешно добавлен! Он уже может отвечать на вопросы",
                    reply_markup=admin_keyboard())
            except TelegramBadRequest:
                new_moder = UncommitedModerator(user_id=id_)
                await message.answer(
                    "Модератор успешно добавлен! Он сможет отвечать на вопросы, как только напишет боту [/start]",
                    reply_markup=admin_keyboard())
            session.add(new_moder)
            session.commit()
        await state.clear()
    else:
        await message.answer(
            "User id пользователя - целое 10-ти значное число. Пожалуйста, введите корректный user id!")


@router.message(F.text, AdminStates.changing_greeting)
async def change_greeting(message: Message, state: FSMContext):
    config.GREETING = message.text
    await state.clear()
    await message.answer(f"""Приветствие успешно изменено на:
<b>{config.GREETING}</b>""", reply_markup=admin_keyboard())


@router.message(F.text == "Удалить модератора", AdminStates.watching_moderators)
async def delete_moderator_request(message: Message, state: FSMContext):
    await state.set_state(AdminStates.delete_moderator)
    await message.answer(f"Введите номер модератора, которого вы хотите разжаловать", reply_markup=cancel_keyboard())


@router.message(F.text.isdigit(), AdminStates.delete_moderator)
async def delete_moderator(message: Message, state: FSMContext, bot: Bot):
    session = db_session.create_session()
    moderator: Moderator = session.query(Moderator).get(int(message.text))
    if moderator is None:
        await message.answer("Пожалуйста, выберите существующего модератора", reply_markup=cancel_keyboard())
        return
    await bot.send_message(moderator.user_id,
                           "К сожалению, вы больше не являетесь модератором хакатона."
                           " Теперь вам доступен функционал обычного пользователя.", reply_markup=faq_keyboard())
    session.delete(moderator)
    all_moderators = session.query(Moderator).all()
    if all_moderators:
        for num, q in enumerate(moderator.questions):
            m = all_moderators[num % len(all_moderators)]
            for old_id in q.message_ids:
                await bot.delete_message(moderator.user_id, old_id.message_id)
                session.delete(old_id)
            msg = await bot.send_message(m.user_id,
                                         **format_with_author(q.sender_name, q.text),
                                         reply_markup=moderator_answer_keyboard(q.id))
            message_id = MessageId(message_id=msg.message_id, question=q.id)
            session.add(message_id)
            m.questions.append(q)
    else:
        for q in moderator.questions:
            for m in q.message_ids:
                await bot.delete_message(moderator.user_id, m.message_id)
                session.delete(m)
            session.delete(q)
    session.commit()
    await state.set_state(AdminStates.watching_moderators)
    await message.answer(f"Модератор {moderator.name} успешно разжалован. Теперь список модераторов выглядит так:")
    await message.answer(format_moderators(), reply_markup=delete_moderator_keyboard())


@router.message(F.text == "Отменить приглашение модератора", AdminStates.watching_moderators)
async def delete_uncommited_moderator_request(message: Message, state: FSMContext):
    await state.set_state(AdminStates.delete_uncommited_moderator)
    await message.answer(f"Введите номер модератора, приглашение которого вы хотите отменить",
                         reply_markup=cancel_keyboard())


@router.message(F.text.isdigit(), AdminStates.delete_uncommited_moderator)
async def delete_uncommited_moderator(message: Message, state: FSMContext):
    session = db_session.create_session()
    moderator = session.query(UncommitedModerator).get(int(message.text))
    if moderator is None:
        await message.answer("Пожалуйста, выберите существующего модератора", reply_markup=cancel_keyboard())
        return
    session.delete(moderator)
    session.commit()
    await state.set_state(AdminStates.watching_moderators)
    await message.answer(f"Приглашение модератора {moderator.id} успешно отменено."
                         f" Теперь список модераторов выглядит так:")
    await message.answer(format_moderators(), reply_markup=delete_moderator_keyboard())


@router.message(F.text == "Отзывы&Пожелания")
async def get_faq(message: Message):
    session = db_session.create_session()
    suggestions = session.query(Suggestion).all()
    if suggestions:
        for s in suggestions:
            await message.answer(**format_with_author(s.sender_name, s.text), reply_markup=admin_keyboard())
    else:
        await message.answer("Пока еще не было оставлено ни одного отзыва или пожелания от пользователей!")


@router.message(F.text == "Добавить модератора")
async def add_moderator_request(message: Message, state: FSMContext):
    await state.set_state(AdminStates.adding_moderator)
    await message.answer("Пожалуйста, пришлите telegram user id модератора!", reply_markup=cancel_keyboard())


@router.message(F.text == "Управление модераторами")
async def control_moderators(message: Message, state: FSMContext):
    await state.set_state(AdminStates.watching_moderators)
    await message.answer(format_moderators(), reply_markup=delete_moderator_keyboard())


@router.message(F.text == "Изменить приветствие")
async def change_greeting_request(message: Message, state: FSMContext):
    await state.set_state(AdminStates.changing_greeting)
    await message.answer(f"""Пожалуйста, пришлите новый текст приветствия! Сейчас оно выглядит так:
<b>{config.GREETING}</b>""", reply_markup=cancel_keyboard())


@router.message(F.text == "Изменить вопросы по умолчанию")
async def get_default_answers_questions(message: Message, state: FSMContext):
    await state.set_state(AdminStates.default_answers_questions)
    await message.answer(format_default_questions(), reply_markup=change_default_questions_keyboard())
