# Счастье в Дом

Телеграм-бот, призванный привлечь внимание к приюту, помочь животным быстрее находить новый дом и упростить процесс взаимодействия с потенциальными хозяевами и благотворителями.


## 🛠️ Стек технологий
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Aiogram](https://img.shields.io/badge/aiogram-%23000.svg?style=for-the-badge&logo=telegram&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/sqlalchemy-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%23316192.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

## 🎯 Быстрый старт
* Склонируйте проект на свой компьютер, используя команду
```
git clone https://github.com/mathusha2023/technoMarchCats
```

* создайте файл `.env.database` в папке catsBot и вставьте туда следующие строки:
```env
POSTGRES_DB=db
POSTGRES_USER=user
POSTGRES_PASSWORD=user
```

* создайте файл `.env.bot` в папке catsBot и вставьте туда следующие строки:
```env
BOT_TOKEN=[Your bot token]
PAYMENTS_TOKEN=[Your payments token]
DATABASE_URL=postgresql://user:user@database/db
SUPERADMIN_ID=[Your telegram id]
DONATE_LINK=[Your donate link]
```

* создайте файл `.env` в папке supportBot и вставьте туда следующие строки:
```env
BOT_TOKEN=[Your bot token]
ADMIN_ID=[Your telegram id]
```

* используйте команды
```
docker-compose build
docker-compose up
```
