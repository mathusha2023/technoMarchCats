from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
import logging
import config
from data import db_session
from handlers import include_routers
from utils.set_commands import set_commands
from utils.add_banned_users_to_cash import add_banned_users_to_cash
from utils.db_pre_init import db_pre_init


async def main():
    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode="html"))
    dp = Dispatcher(storage=MemoryStorage())
    include_routers(dp)  # добавляем все обработчики событий
    await bot.delete_webhook(drop_pending_updates=True)
    await set_commands(bot)  # создаем боковое меню бота с командами
    try:
        await dp.start_polling(bot)
    except asyncio.exceptions.CancelledError:
        logging.info("The polling cycle was interrupted")


if __name__ == "__main__":
    db_session.global_init(config.DATABASE_URL)  # инициализация базы данных
    db_pre_init()  # добавление базовых тегов в базу данных, если их там нет
    add_banned_users_to_cash()  # добавление заблокированных пользователей из базы данных в кеш
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())