from aiogram import Dispatcher
from .commands_handlers import router as commands_router
from .default_callback_handlers import router as default_callback_router
from .admin import animals_callback_router, add_animal_router, delete_animal_router, update_animal_router, guardianship_router, users_control_router, users_control_callback_router, publish_news_callback_router, publish_news_router, stats_callback, publish_volunteer_news_callback_router, publish_volunteer_news_router
from .user import users_callback_router, watch_animals_handler, test_router, test_callback_router


def include_routers(dp: Dispatcher):
    dp.include_routers(commands_router, default_callback_router, animals_callback_router, add_animal_router,
                       users_callback_router, watch_animals_handler, delete_animal_router, update_animal_router, guardianship_router, users_control_router, users_control_callback_router,  publish_news_callback_router, publish_news_router, stats_callback, publish_volunteer_news_router, publish_volunteer_news_callback_router, test_router)
