from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from filters import AdminFilter
from states import AdminStates
from keyboards import cancel_keyboard, change_default_questions_keyboard
from utils import format_default_questions
import config

router = Router()
router.message.filter(AdminFilter())


@router.message(F.text == "Изменить ответы", AdminStates.default_answers_questions)
async def f(message: Message, state: FSMContext):
    if config.QUESTIONS:
        await message.answer("Укажите номер вопроса, ответ на который вы желаете изменить",
                             reply_markup=cancel_keyboard())
        await state.set_state(AdminStates.change_questions)
    else:
        await message.answer("В настоящий момент вопросы отсутствуют")


@router.message(F.text.isdigit(), AdminStates.change_questions)
async def f(message: Message, state: FSMContext):
    num = int(message.text)
    if num > len(config.QUESTIONS):
        await message.answer("Пожалуйста, введите существующее число!", reply_markup=cancel_keyboard())
    else:
        await message.answer("Введите новый ответ на вопрос",
                             reply_markup=cancel_keyboard())
        await state.set_state(AdminStates.editing_question)
        await state.update_data(num=num - 1)


@router.message(F.text, AdminStates.editing_question)
async def f(message: Message, state: FSMContext):
    num = (await state.get_data())["num"]
    for n, q in enumerate(config.QUESTIONS):
        if n == num:
            config.QUESTIONS[q] = message.text
            break
    await message.answer("Успешно! Теперь вопросы выглядят так:")
    await state.set_data({})
    await state.set_state(AdminStates.default_answers_questions)
    await message.answer(format_default_questions(), reply_markup=change_default_questions_keyboard())


@router.message(F.text == "Добавить вопрос/ответ", AdminStates.default_answers_questions)
async def f(message: Message, state: FSMContext):
    await message.answer("Введите новый вопрос",
                         reply_markup=cancel_keyboard())
    await state.set_state(AdminStates.adding_question)


@router.message(F.text, AdminStates.adding_question)
async def f(message: Message, state: FSMContext):
    if message.text not in config.QUESTIONS:
        await message.answer("Введите ответ на него", reply_markup=cancel_keyboard())
        await state.set_state(AdminStates.adding_answer)
        await state.update_data(question=message.text)
    else:
        await message.answer("Такой вопрос уже существует! Пожалуйста, введите новый вопрос.",
                             reply_markup=cancel_keyboard())


@router.message(F.text, AdminStates.adding_answer)
async def f(message: Message, state: FSMContext):
    q = (await state.get_data())["question"]
    config.QUESTIONS[q] = message.text
    await message.answer("Успешно! Теперь вопросы выглядят так:")
    await state.set_data({})
    await state.set_state(AdminStates.default_answers_questions)
    await message.answer(format_default_questions(), reply_markup=change_default_questions_keyboard())


@router.message(F.text == "Удалить вопрос", AdminStates.default_answers_questions)
async def f(message: Message, state: FSMContext):
    if config.QUESTIONS:
        await message.answer("Укажите номер вопроса, который вы желаете удалить", reply_markup=cancel_keyboard())
        await state.set_state(AdminStates.deleting_question)
    else:
        await message.answer("В настоящий момент вопросы отсутствуют")


@router.message(F.text.isdigit(), AdminStates.deleting_question)
async def f(message: Message, state: FSMContext):
    num = int(message.text)
    if num > len(config.QUESTIONS):
        await message.answer("Пожалуйста, введите существующее число!", reply_markup=cancel_keyboard())
    else:
        for n, q in enumerate(config.QUESTIONS):
            if n == num - 1:
                del config.QUESTIONS[q]
                break
        await message.answer("Успешно! Теперь вопросы выглядят так:")
        await state.set_data({})
        await state.set_state(AdminStates.default_answers_questions)
        await message.answer(format_default_questions(), reply_markup=change_default_questions_keyboard())
