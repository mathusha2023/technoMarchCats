from data import db_session
from data.moderators import Moderator
from data.uncommited_moderators import UncommitedModerator


def format_moderators():
    res = "Модераторы хакатона:\n"
    session = db_session.create_session()
    true_moderators = session.query(Moderator).all()
    uncommited_moderators = session.query(UncommitedModerator).all()
    for m in true_moderators:
        s = f"{m.id}. {m.name} - {m.user_id}. Вопросов в очереди: {len(m.questions)}\n"
        res += s
    res += "\n############################################\n\n"
    res += "Приглашения отправлены модераторам:\n"
    for m in uncommited_moderators:
        s = f"{m.id}. User id {m.user_id}\n"
        res += s
    return res
