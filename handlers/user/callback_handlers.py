from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy import desc

import keyboards
from data.animals_filters import AnimalFilter
from data.animals_tags import AnimalTag
from data.db_session import create_session
from data.users import User
from states import WatchAnimalsStates
from utils.generate_animal_filter_message import generate_animal_filter_message
from utils.generate_next_animal_card import generate_next_animal_card

router = Router()


@router.callback_query(F.data == "watch_animals")
async def cats_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(WatchAnimalsStates.watching)
    await callback.message.answer("Вот наши пушистые друзья. Может быть, вам кто-нибудь приглянется?",
                                  reply_markup=keyboards.watch_animals_keyboard())
    await generate_next_animal_card(callback.from_user.id, callback.message)
    await callback.answer()


@router.callback_query(F.data == "change_gender_filter")  # изменение пола животного на фильтре
async def change_gender_filter_callback(callback: CallbackQuery):
    session = create_session()
    animal_filter: AnimalFilter = session.query(User).where(User.id == callback.from_user.id).first().filter
    animal_filter.gender = (animal_filter.gender + 1) % 3
    session.commit()
    await generate_animal_filter_message(callback.message, animal_filter, edit=True)
    await callback.answer()


@router.callback_query(F.data.startswith("tags_filter_left_"))  # перелистывание списка тегов влево по кнопке
async def tags_filter_left__callback(callback: CallbackQuery):
    fourth_number = int(callback.data.split("_")[-1])  # получаем номер последней четверки, в которой находился тег
    session = create_session()
    tags = session.query(AnimalTag).limit(4).offset((fourth_number - 2 if fourth_number > 1 else 0) * 4).all()
    string_tags = [tag.tag for tag in tags]
    await callback.message.edit_reply_markup(
        reply_markup=keyboards.animal_tags_filter_keyboard(string_tags, fourth_number - 1, show_right=True, show_left=tags[-1].id > 4))
    await callback.answer()


@router.callback_query(F.data.startswith("tags_filter_right_"))  # перелистывание списка тегов вправо по кнопке
async def tags_filter_right__callback(callback: CallbackQuery):
    fourth_number = int(callback.data.split("_")[-1])  # получаем номер последней четверки, в которой находился тег
    session = create_session()
    last_tag = session.query(AnimalTag).order_by(desc(AnimalTag.id)).first()
    tags = session.query(AnimalTag).limit(4).offset(fourth_number * 4).all()
    string_tags = [tag.tag for tag in tags]
    await callback.message.edit_reply_markup(
        reply_markup=keyboards.animal_tags_filter_keyboard(string_tags, fourth_number + 1, show_left=True, show_right=last_tag.id > tags[-1].id))
    await callback.answer()


@router.callback_query(F.data.startswith("tags_filter_"))  # пользователь нажал на название тега на клавиатуре выбора тегов
async def tags_filter__callback(callback: CallbackQuery):
    tag_name = callback.data.split("_")[-1]  # получаем название тега
    session = create_session()
    animal_filter = session.query(User).where(User.id == callback.from_user.id).first().filter
    tag = session.query(AnimalTag).where(AnimalTag.tag == tag_name).first()

    if tag in animal_filter.tags:
        animal_filter.tags.remove(tag)
    else:
        animal_filter.tags.append(tag)
    session.commit()

    await generate_animal_filter_message(callback.message, animal_filter, edit=True, add_keyboard=False)
    await callback.answer()


@router.callback_query(F.data == "change_tags_filter")  # нажатие кнопки "изменить теги" - генерация клавиатуры для смены тегов
async def change_tags_filter_callback(callback: CallbackQuery):
    session = create_session()
    last_tag = session.query(AnimalTag).order_by(desc(AnimalTag.id)).first()
    tags = session.query(AnimalTag).limit(4).all()
    string_tags = [tag.tag for tag in tags]
    await callback.message.edit_reply_markup(
        reply_markup=keyboards.animal_tags_filter_keyboard(string_tags, 1, show_right=last_tag.id > tags[-1].id))
    await callback.answer()


@router.callback_query(F.data == "back_filter")  # нажатие кнопки назад при смене тегов
async def back_filter_callback(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=keyboards.animal_filter_keyboard())
    await callback.answer()


@router.callback_query(F.data == "min_age_down_filter")
async def min_age_down_filter_callback(callback: CallbackQuery):
    session = create_session()
    animal_filter: AnimalFilter = session.query(User).where(User.id == callback.from_user.id).first().filter
    if animal_filter.minAge == 0:
        return callback.answer("Возраст не может быть ниже 0!")
    animal_filter.minAge -= 1
    session.commit()
    await generate_animal_filter_message(callback.message, animal_filter, edit=True)
    await callback.answer()


@router.callback_query(F.data == "min_age_up_filter")
async def min_age_up_filter_callback(callback: CallbackQuery):
    session = create_session()
    animal_filter: AnimalFilter = session.query(User).where(User.id == callback.from_user.id).first().filter
    if animal_filter.minAge == animal_filter.maxAge:
        return callback.answer("Минимальный возраст не может быть выше максимального!")
    animal_filter.minAge += 1
    session.commit()
    await generate_animal_filter_message(callback.message, animal_filter, edit=True)
    await callback.answer()


@router.callback_query(F.data == "max_age_down_filter")
async def max_age_down_filter_callback(callback: CallbackQuery):
    session = create_session()
    animal_filter: AnimalFilter = session.query(User).where(User.id == callback.from_user.id).first().filter
    if animal_filter.minAge == animal_filter.maxAge:
        return callback.answer("Максимальный возраст не может быть ниже минимального!")
    animal_filter.maxAge -= 1
    session.commit()
    await generate_animal_filter_message(callback.message, animal_filter, edit=True)
    await callback.answer()


@router.callback_query(F.data == "max_age_up_filter")
async def max_age_up_filter_callback(callback: CallbackQuery):
    session = create_session()
    animal_filter: AnimalFilter = session.query(User).where(User.id == callback.from_user.id).first().filter
    animal_filter.maxAge += 1
    session.commit()
    await generate_animal_filter_message(callback.message, animal_filter, edit=True)
    await callback.answer()
