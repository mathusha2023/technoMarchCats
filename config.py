import os
from dotenv import load_dotenv

load_dotenv(".env.bot")

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
SUPERADMIN_ID = int(os.getenv("SUPERADMIN_ID"))

BOT_COMMANDS = {"start": "Запуск бота",
                "help": "Показать список команд",
                "about": "Информация о приюте",
                "admin": "Админ-панель (только для администраторов!)"}  # все команды бота и описания к ним
