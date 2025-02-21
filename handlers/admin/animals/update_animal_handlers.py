from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from datetime import datetime
from data import db_session
import keyboards
import strings
from data.animals import Animal
from data.animals_tags import AnimalTag
from filters import StatesGroupFilter
from middlewares import MediaGroupMiddleware
from states import UpdateAnimalStates
from utils.generate_animal_card_by_state import generate_animal_card_by_state
from utils.update_animal_information import update_animal_information

router = Router()
router.message.middleware(MediaGroupMiddleware())


@router.message(F.text == "В меню",
                StatesGroupFilter(UpdateAnimalStates))  # сработает при любом состоянии обновления животного
async def back(message: Message, state: FSMContext):  # полная отмена редактирования информации о животных
    await state.clear()
    await message.answer("Редактирование котика отменено", reply_markup=keyboards.ReplyKeyboardRemove())
    await message.answer(strings.ADMIN_MENU_CAPTION, reply_markup=keyboards.admin_menu_keyboard())


@router.message(F.text == "Отмена",
                StatesGroupFilter(UpdateAnimalStates))  # сработает при любом состоянии обновления животного
async def cancel(message: Message, state: FSMContext):  # отмена изменения какого-то конкретного параметра кота
    await state.set_state(UpdateAnimalStates.choose_change_param)
    await message.answer(f"Какую информацию вы хотите обновить?", reply_markup=keyboards.admin_update_animal_keyboard())


@router.message(F.text.isdigit(), UpdateAnimalStates.index_input)
async def update_animal(message: Message, state: FSMContext):
    animal_id = int(message.text)
    session = db_session.create_session()
    animal = session.query(Animal).where(Animal.id == animal_id).first()
    if animal is None:
        return await message.answer(f"Животного с ID {animal_id} не существует! Введите существующий ID",
                                    reply_markup=message.reply_markup)

    list_images = [image.image for image in animal.images]
    data = {"session": session, "id": animal_id, "name": animal.name, "gender": animal.gender,
            "birthday": animal.birthDate,
            "description": animal.description, "photos": list_images, "tags": animal.tags}

    await state.set_data(data)
    await state.set_state(UpdateAnimalStates.choose_change_param)
    await message.answer(f"Карточка {animal.name} сейчас выглядит так:")
    await generate_animal_card_by_state(data, message)
    await message.answer(f"Какую информацию вы хотите обновить?", reply_markup=keyboards.admin_update_animal_keyboard())


@router.message(UpdateAnimalStates.index_input)
async def delete_animal(message: Message):
    await message.answer("Введите корректный ID животного!")


@router.message(F.text == "Сохранить", UpdateAnimalStates.choose_change_param)
async def save_animal(message: Message, state: FSMContext):
    data = await state.get_data()

    await update_animal_information(data)

    await message.answer(f"Карточка {data['name']} сейчас выглядит так:", reply_markup=keyboards.ReplyKeyboardRemove())
    await generate_animal_card_by_state(data, message)

    await state.set_state(UpdateAnimalStates.index_input)
    await state.set_data({})
    await message.answer("Введите ID животного, информацию о котором вы хотите обновить",
                         reply_markup=keyboards.watch_animals_ids_keyboard())


@router.message(F.text == "Имя", UpdateAnimalStates.choose_change_param)
async def delete_animal(message: Message, state: FSMContext):
    await state.set_state(UpdateAnimalStates.naming)
    await message.answer("Пожалуйста, пришлите новое имя котика", reply_markup=keyboards.cancel_keyboard())


@router.message(F.text == "Пол", UpdateAnimalStates.choose_change_param)
async def delete_animal(message: Message, state: FSMContext):
    await state.set_state(UpdateAnimalStates.changing_gender)
    await message.answer("Пожалуйста, пришлите новый пол котика. 1 - мальчик, 2 - девочка",
                         reply_markup=keyboards.select_animal_gender_keyboard())


@router.message(F.text == "Дату рождения", UpdateAnimalStates.choose_change_param)
async def delete_animal(message: Message, state: FSMContext):
    await state.set_state(UpdateAnimalStates.changing_birthday)
    await message.answer("Пожалуйста, пришлите новую дату рождения котика в формате dd.mm.yyyy",
                         reply_markup=keyboards.cancel_keyboard())


@router.message(F.text == "Описание", UpdateAnimalStates.choose_change_param)
async def delete_animal(message: Message, state: FSMContext):
    await state.set_state(UpdateAnimalStates.describing)
    await state.update_data({"description": message.text})
    await message.answer("Пожалуйста, пришлите новое описание котика", reply_markup=keyboards.cancel_keyboard())


@router.message(F.text == "Фотографии", UpdateAnimalStates.choose_change_param)
async def delete_animal(message: Message, state: FSMContext):
    await state.set_state(UpdateAnimalStates.changing_images)
    await message.answer("Пожалуйста, пришлите новые фотографии котика (до 10 штук)",
                         reply_markup=keyboards.cancel_keyboard())


@router.message(F.text == "Теги", UpdateAnimalStates.choose_change_param)
async def delete_animal(message: Message, state: FSMContext):
    await state.set_state(UpdateAnimalStates.changing_tags)
    await message.answer(
        "Пожалуйста выберите новые теги котика из списка ниже. Пришлите их номера через пробел. Например, 1 2 3 8",
        reply_markup=keyboards.cancel_keyboard())
    s = ""
    data = await state.get_data()
    session = data["session"]
    tags = session.query(AnimalTag).order_by(AnimalTag.id).all()
    for tag in tags:
        s += f"{tag.id} - {tag.tag}\n"
    await message.answer(s)


@router.message(F.text, UpdateAnimalStates.naming)
async def delete_animal(message: Message, state: FSMContext):
    await state.update_data({"name": message.text})
    data = await state.get_data()
    await message.answer(f"Карточка {data['name']} теперь выглядит так:")
    await generate_animal_card_by_state(data, message)
    await cancel(message, state)


@router.message(F.text.in_(["1", "2"]), UpdateAnimalStates.changing_gender)  # корректный ввод для смены пола кота
async def delete_animal(message: Message, state: FSMContext):
    await state.update_data({"gender": int(message.text) - 1})
    data = await state.get_data()
    await message.answer(f"Карточка {data['name']} теперь выглядит так:")
    await generate_animal_card_by_state(data, message)
    await cancel(message, state)


@router.message(F.text, UpdateAnimalStates.changing_gender)  # некорректные данные
async def delete_animal(message: Message):
    await message.answer("Пришлите 1, если у нас мальчик, и 2 - если девочка!")


@router.message(F.text, UpdateAnimalStates.changing_birthday)
async def changing_age(message: Message, state: FSMContext):
    try:
        date_ = datetime.strptime(message.text, "%d.%m.%Y").date()
        await state.update_data({"birthday": date_})
        data = await state.get_data()
        await message.answer(f"Карточка {data['name']} теперь выглядит так:")
        await generate_animal_card_by_state(data, message)
        await cancel(message, state)
    except ValueError:
        await message.answer("Введите дату рождения в требуемом формате!")


@router.message(F.text, UpdateAnimalStates.describing)
async def delete_animal(message: Message, state: FSMContext):
    await state.update_data({"description": message.text})
    data = await state.get_data()
    await message.answer(f"Карточка {data['name']} теперь выглядит так:")
    await generate_animal_card_by_state(data, message)
    await cancel(message, state)


@router.message(UpdateAnimalStates.changing_images)  # замена фотографий
async def changing_images(message: Message, state: FSMContext, album: [Message] = None):
    photos = []
    if album is None:  # если фотографии не были присланы группой
        album = [message]
    for element in album:  # получаем фотографии из всех элементов альбома
        if element.photo:
            photos.append(element.photo[-1].file_id)
    if len(photos) > 10:  # можно прислать не более 10 фотографий, лишние удаляются
        photos = photos[:10]
    if not photos:
        return await message.answer("Пришлите от одной до десяти фотографий котика!")

    await state.update_data({"photos": photos})
    data = await state.get_data()
    await message.answer(f"Карточка {data['name']} теперь выглядит так:")
    await generate_animal_card_by_state(data, message)
    await cancel(message, state)


@router.message(F.text, UpdateAnimalStates.changing_tags)
async def changing_tags(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        tags = []
        session = data["session"]
        indexes = map(int, message.text.split())
        for i in indexes:
            tag = session.query(AnimalTag).where(AnimalTag.id == i).first()
            if tag is None:
                raise ValueError
            tags.append(tag)
        await state.update_data({"tags": tags})
        data["tags"] = tags
        await message.answer(f"Карточка {data['name']} теперь выглядит так:")
        await generate_animal_card_by_state(data, message)
        await cancel(message, state)

    except ValueError:
        await message.answer("Пришлите корректные номера тегов!")