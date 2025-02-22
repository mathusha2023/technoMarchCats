from data import db_session
from config import BANNED_USERS
from data.users import User


def add_banned_users_to_cash():
    session = db_session.create_session()
    banned_users = session.query(User).where(User.isBanned).all()
    BANNED_USERS.extend([user.id for user in banned_users])
