import logging

from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery, Message

import config
import strings
import keyboards
from filters import BannedFilter
from data.db_session import create_session
from data.users import User

router = Router()


@router.message(BannedFilter())
async def answer_for_banned(callback: CallbackQuery):
    await callback.message.answer(strings.BANNED_USERS_MESSAGE, reply_markup=keyboards.ReplyKeyboardRemove())


@router.callback_query(F.data == "contact")
async def contact_callback(callback: CallbackQuery):
    await callback.message.edit_text(strings.CONTACTS, reply_markup=keyboards.about_keyboard())


@router.callback_query(F.data == "about")
async def about_callback(callback: CallbackQuery):
    await callback.message.edit_text(strings.INFO, reply_markup=keyboards.contacts_keyboard())


@router.callback_query(F.data == "start_contact")
async def start_contact_callback(callback: CallbackQuery):
    await callback.message.edit_text(strings.CONTACTS, reply_markup=keyboards.to_start_menu_keyboard())


@router.callback_query(F.data == "start_about")
async def start_about_callback(callback: CallbackQuery):
    await callback.message.edit_text(strings.INFO, reply_markup=keyboards.to_start_menu_keyboard())


@router.callback_query(F.data == "fast_pay")
async def fast_pay_callback(callback: CallbackQuery):
    price = LabeledPrice(label="Поддержать приют", amount=config.PAYMENT_PRICE * 100)  # в копейках (руб)

    await callback.message.answer_invoice(
                           title="Поддержать приют",
                           description="Поддержать приют копейкой",
                           provider_token=config.PAYMENTS_TOKEN,
                           currency="rub",
                           photo_url="https://cs6.livemaster.ru/storage/51/8d/e9304e78c01418b5ea956d3be36a.jpg",
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[price],
                           start_parameter="one-month-subscription",
                           payload="test-invoice-payload")

    await callback.answer()


# pre checkout  (must be answered in 10 seconds)
@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
    await pre_checkout_q.answer(ok=True)


# successful payment
@router.message(F.successful_payment)
async def successful_payment(message: Message):
    logging.info("SUCCESSFUL PAYMENT!")
    payment_info = message.successful_payment.json()
    logging.debug(payment_info)
    await message.answer(f"Спасибо! Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!")


@router.callback_query(F.data == "help_um")
async def help_up_callback(callback: CallbackQuery):
    session = create_session()
    user = session.query(User).where(User.id == callback.from_user.id).first()

    await callback.message.edit_text(strings.HELP, reply_markup=keyboards.help_um_keyboard(user.isVolunteer))


@router.callback_query(F.data == "start")
async def start_callback(callback: CallbackQuery):
    await callback.message.edit_text(strings.GREETING, reply_markup=keyboards.start_keyboard())
