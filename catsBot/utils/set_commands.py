from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
import config


# список команд в боковом меню бота
async def set_commands(bot: Bot):
    commands = list(map(lambda x: BotCommand(command=x[0], description=x[1]), config.BOT_COMMANDS.items()))
    await bot.set_my_commands(commands, BotCommandScopeDefault())
