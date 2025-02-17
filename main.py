from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
import logging
import config
from data import db_session
from handlers import include_routers


async def main():
    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode="html"))
    dp = Dispatcher(storage=MemoryStorage())
    include_routers(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    except asyncio.exceptions.CancelledError:
        print("The polling cycle was interrupted")


if __name__ == "__main__":
    db_session.global_init(config.DATABASE_URL)
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
