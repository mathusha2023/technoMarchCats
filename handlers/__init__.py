from aiogram import Dispatcher
from .default_handlers import router as default_router

def include_routers(dp: Dispatcher):
    dp.include_routers(default_router)
