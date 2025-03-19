from aiogram.filters import BaseFilter
from aiogram.types import Message
from data import db_session
from data.uncommited_moderators import UncommitedModerator


class UncommitedModeratorFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        session = db_session.create_session()
        moders = session.query(UncommitedModerator).all()
        for m in moders:
            if m.user_id == message.from_user.id:
                return True
        return False
