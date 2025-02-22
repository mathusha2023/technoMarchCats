import os
import json
from dotenv import load_dotenv

load_dotenv(".env.bot")

BOT_TOKEN = "8126780421:AAF45Ybbb4blXsz2ur22siaAWd-XyoyTNRY"#os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
SUPERADMIN_ID = 1442472877#int(os.getenv("SUPERADMIN_ID"))
CONFIG_FILE = os.getenv("CONFIG_FILE", "config.json")

with open(CONFIG_FILE, encoding="utf-8") as file:
    jsonFile = json.load(file)

BOT_COMMANDS = jsonFile["botCommands"]
ANIMAL_TAGS = jsonFile["animalTags"]
