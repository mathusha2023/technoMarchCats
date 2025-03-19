from config import QUESTIONS


def format_default_questions():
    res = ""
    for i, q in enumerate(QUESTIONS, start=1):
        s = f"{i}. <b>{q}</b> - <u>{QUESTIONS[q]}</u>\n"
        res += s
    return res if res else "В настоящий момент вопросы отсутствуют"
