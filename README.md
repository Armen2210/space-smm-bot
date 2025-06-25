# 🚀 Космический SMM-бот для Telegram

Проект автоматически публикует посты и изображения о космических путешествиях в Telegram-канал.  
Посты генерируются с помощью GPT-4o, изображения — через DALL·E 3.

---

## 🔧 Функции

- Генерация текстов от лица космотуриста по заранее заданному расписанию.
- Создание реалистичных изображений локаций.
- Публикация постов вручную через Telegram (`/new_post`).
- Автоматическая публикация через HTTP-запрос (`/publish`) — интеграция с Make.
- Защита от сбоев, логирование, централизованная логика публикации.

---

## 🗂 Структура проекта

project-root/
├── bot.py # Ручной запуск бота через Telegram
├── .env # Переменные окружения
├── schedule_2025_unique.json # Расписание тем постов по датам
├── utils/
│ └── post_utils.py # Генерация постов, изображений и отправка
├── scheduler/
│ └── trigger.py # Синхронный запуск публикации
│ └── server.py # HTTP-сервер для Make и Render

---

## 📦 Установка

```bash
git clone https://github.com/yourusername/space-smm-bot.git
cd space-smm-bot
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt


🔐 Настройка .env
Создайте файл .env и заполните переменные:

TELEGRAM_TOKEN=ваш_токен_бота
OPENAI_API_KEY=ваш_ключ_OpenAI
TARGET_CHAT_ID=123456789
PORT=5000


🚀 Запуск
Бот (ручной запуск):
python bot.py

Сервер для Make / Render:
python scheduler/server.py

Тест публикации вручную:
curl -X POST http://localhost:5000/publish



📅 Расписание тем
Файл schedule_2025_unique.json содержит список тем по датам:
[
  {
    "date": "2025-06-25",
    "topic": "Пляж с чёрным льдом на Хароне"
  },
  {
    "date": "2025-06-26",
    "topic": "Лаборатория будущего на Церере"
  }
]


⚙️ Используемые технологии
Python 3.10+

OpenAI GPT-4o

DALL·E 3

python-telegram-bot

Flask (HTTP-сервер)

httpx + dotenv


🧠 Автор
Проект реализован Арменом Амбарцумяном при поддержке AI-инженера GPT-4о.
Все идеи, визуальные стили и сценарии — авторские, вдохновлённые темой космотуризма.