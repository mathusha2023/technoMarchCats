from aiogram import Dispatcher
from .default_handlers import router as default_router
from .default_callback_handlers import router as default_callback_router

def include_routers(dp: Dispatcher):
    dp.include_routers(default_router, default_callback_router)
