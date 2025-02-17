from aiogram import Dispatcher
from .commands_handlers import router as commands_router
from .default_callback_handlers import router as default_callback_router
from .admin import animals_callback_router

def include_routers(dp: Dispatcher):
    dp.include_routers(commands_router, default_callback_router, animals_callback_router)
