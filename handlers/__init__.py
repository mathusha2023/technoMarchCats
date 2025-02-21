from aiogram import Dispatcher
from .commands_handlers import router as commands_router
from .default_callback_handlers import router as default_callback_router
from .admin import animals_callback_router, add_animal_router, delete_animal_router
from .user import users_callback_router, watch_animals_handler


def include_routers(dp: Dispatcher):
    dp.include_routers(commands_router, default_callback_router, animals_callback_router, add_animal_router,
                       users_callback_router, watch_animals_handler, delete_animal_router)
