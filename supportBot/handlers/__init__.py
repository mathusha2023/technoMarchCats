from aiogram import Dispatcher
from .admin_handlers import router as admin_router
from .moderator_handlers import router as moder_router
from .user_handlers import router as user_router
from .default_questions_settings import router as q_router
from .no_such_variant_handler import router as except_router


def include_routers(dp: Dispatcher):
    dp.include_routers(admin_router, q_router, moder_router, user_router, except_router)
