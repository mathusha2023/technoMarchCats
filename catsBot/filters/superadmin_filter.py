from aiogram.filters import BaseFilter
from aiogram.types import Message
import config


#  фильтр на права доступа к функциям супер-админа
class SuperAdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == config.SUPERADMIN_ID