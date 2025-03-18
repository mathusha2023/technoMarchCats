import os
import json
from dotenv import load_dotenv

load_dotenv(".env.bot")

BOT_TOKEN = os.getenv("BOT_TOKEN")
PAYMENTS_TOKEN = os.getenv("PAYMENTS_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
SUPERADMIN_ID = int(os.getenv("SUPERADMIN_ID"))
DONATE_LINK = os.getenv("DONATE_LINK", "https://vk.com/topic-88538029_31812031")
CONFIG_FILE = os.getenv("CONFIG_FILE", "config.json")

with open(CONFIG_FILE, encoding="utf-8") as file:
    jsonFile = json.load(file)

BOT_COMMANDS = jsonFile["botCommands"]
ANIMAL_TAGS = jsonFile["animalTags"]
PAYMENT_PRICE = jsonFile["paymentPrice"]

BANNED_USERS = list()
