# 🚀 Космический SMM-бот для Telegram

**Автоматический Telegram-бот для генерации и публикации контента о путешествиях, а также сбора аналитики просмотров.**

## ✨ Функционал

✅ Генерация текстовых постов с помощью OpenAI GPT  
✅ Генерация изображений с помощью DALL·E  
✅ Автоматическая публикация в Telegram-канале или группе  
✅ Сохранение информации о каждом посте (`message_id`, тема, дата)  
✅ Сбор статистики просмотров и комментариев через Telethon  
✅ Отдача аналитики через HTTP API  
✅ Интеграция с Make (Integromat) для автоматизации процессов  

---

## 🛠️ Технологии

- **Python 3**
- Flask
- Telethon
- OpenAI API
- Telegram Bot API
- Make (Integromat)
- Render (деплой)

---

## ⚙️ Структура проекта

├── scheduler/
│ ├── server.py # Flask сервер с API
│ ├── trigger.py # Запуск публикации из консоли
├── utils/
│ └── post_utils.py # Логика генерации и публикации постов
├── analytics_collector.py # Сбор аналитики просмотров через Telethon
├── schedule_2025_unique.json # План публикаций
├── messages_log.json # Лог опубликованных сообщений
├── analytics_log.json # Лог аналитики просмотров
├── bot.py # Telegram бот с командой /new_post
├── .env # Конфигурация окружения

---

## 📦 Установка

```bash
git clone https://github.com/yourusername/space-smm-bot.git
cd space-smm-bot
python -m venv .venv

✅ Активация виртуального окружения:
🔹 Linux / macOS:
bash
Копировать
Редактировать
source .venv/bin/activate
🔹 Windows:
powershell
Копировать
Редактировать
.venv\Scripts\activate
✅ Установка зависимостей:
bash
Копировать
Редактировать
pip install -r requirements.txt


🔐 Настройка .env
Создайте файл .env и заполните переменные:

TELEGRAM_TOKEN=токен_бота
OPENAI_API_KEY=твой_openai_api_key
TARGET_CHAT_ID=ID_группы_или_канала
PUBLISH_SECRET=секретный_ключ_для_запросов

TELETHON_API_ID=api_id_telegram
TELETHON_API_HASH=api_hash_telegram


🚀 Запуск
✅ Бот (ручной запуск):
bash
Копировать
Редактировать
python bot.py

✅ Сервер для Make / Render:
bash
Копировать
Редактировать
python scheduler/server.py

✅ Тест публикации вручную через curl:
bash
Копировать
Редактировать
curl -X POST https://<твой-домен>.onrender.com/publish -H "X-Auth-Token: <твой_секретный_ключ>"
(замени <твой-домен> и <твой_секретный_ключ> на свои значения)

✅ Сбор аналитики просмотров:
bash
Копировать
Редактировать
python analytics_collector.py

📅 Расписание тем
Файл schedule_2025_unique.json содержит список тем по датам:

json
Копировать
Редактировать
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
httpx
python-dotenv
Telethon (для аналитики просмотров)

🧠 Автор
Проект реализован Арменом Амбарцумяном при поддержке AI-инженера GPT-4о.
Все идеи, визуальные стили и сценарии — авторские, вдохновлённые темой космотуризма.
