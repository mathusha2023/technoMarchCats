from aiogram.filters import BaseFilter
from aiogram.types import Message
import config


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == config.ADMIN_ID
