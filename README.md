# Letters 🕵️‍♂️✉️

Одноразовые письма, как в PrivNote.
Пользователь пишет сообщение, получает уникальную ссылку, и может передать её другому.
Как только письмо прочитано — оно исчезает.

## 🔧 Технологии

- Python 3.12
- Flask + Flask-RESTx
- Peewee (ORM)
- PostgreSQL
- HTML + CSS (ручной фронт)
- Pydantic (валидация)

## 🚀 Как запустить

1. Склонируй проект:
git clone https://github.com/your_username/secret-letter-box.git
cd secret-letter-box

2. Создай .env файл
SECRET_KEY = "My_Secret_Key"
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password

3. Установи зависимости:
pip install -r requirements.txt

4. Запусти приложение:
flask run

✅ Возможности
Создание письма через форму
Генерация уникальной ссылки
Однократное открытие письма
Автоматическое удаление после прочтения
Отображение времени, прошедшего с момента прочтения
