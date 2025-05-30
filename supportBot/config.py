from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = int(os.getenv("ADMIN_ID"))

GREETING = "Здравствуй, дорогой посетитель приюта \"Счастья в дом\"! 👋 Здесь ты сможешь 📩 Задать вопросы и внести свои предложения по поводу улучшения работы нашего приюта. 📨"

QUESTIONS = {"Какой корм купить для приюта?": "🔹 Сухие и влажные корма линейки ROYAL CANIN - Urinary S/O High Dilution, GASTRO INTESTINAL, BABYCAT, KITTEN;\n🔹 Влажный корм ШЕБА;\n🔹 Сухой корм ФАРМИНА.",
             "Что можно принести в приют из вещей?": "🔹 Лотки;\n🔹 Миски;\n🔹Поилки;\n🔹 Игрушки;\n🔹 Подстилки;\n🔹 Коврики;\n(список не конечный)",
             "Можно ли забрать всех котов сразу?": "Конечно, можно! Но вы должны понимать, что уход за пушистыми друзьями - серьезная ответственность!",
             "Сколько стоит забрать котика из приюта?": "Забрать пушистика можно совершенно бесплатно! Отдаем котиков в добрые руки!", }
