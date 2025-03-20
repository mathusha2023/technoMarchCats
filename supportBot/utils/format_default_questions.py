from config import QUESTIONS


# возвращает в виде текста часто задаваемые вопросы с ответами
def format_default_questions():
    res = ""
    for i, q in enumerate(QUESTIONS, start=1):
        s = f"{i}. <b>{q}</b>\n{QUESTIONS[q]}\n\n"
        res += s
    return res if res else "В настоящий момент вопросы отсутствуют"
