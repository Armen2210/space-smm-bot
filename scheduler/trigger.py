# scheduler/trigger.py

import sys
import os
import logging
from dotenv import load_dotenv
from telegram import Bot
from openai import OpenAI
from utils.post_utils import send_post_to_telegram
import httpx

# ✅ Отладочный вывод
print("✅ trigger.py запущен")
logging.basicConfig(level=logging.INFO)
logging.info("✅ trigger.py запущен (логгер работает)")

# 📂 Добавляем корень проекта в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Загрузка переменных окружения
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TARGET_CHAT_ID = os.getenv("TARGET_CHAT_ID")

# Показываем переменные (в логах Render увидишь)
print(f"🔑 TELEGRAM_TOKEN = {bool(TELEGRAM_TOKEN)}")
print(f"🔑 OPENAI_API_KEY = {bool(OPENAI_API_KEY)}")
print(f"🔑 TARGET_CHAT_ID = {TARGET_CHAT_ID}")

# Проверка наличия всех переменных
assert TELEGRAM_TOKEN, "⛔ TELEGRAM_TOKEN не задан"
assert OPENAI_API_KEY, "⛔ OPENAI_API_KEY не задан"
assert TARGET_CHAT_ID, "⛔ TARGET_CHAT_ID не задан"

# Инициализация клиентов
timeout_config = httpx.Timeout(60.0, connect=10.0)
openai_client = OpenAI(api_key=OPENAI_API_KEY, timeout=timeout_config)
telegram_bot = Bot(token=TELEGRAM_TOKEN)

def run():
    try:
        print("▶️ Вход в функцию run()")
        logging.info("▶️ Вход в функцию run()")

        send_post_to_telegram(
            client=openai_client,
            bot=telegram_bot,
            chat_id=int(TARGET_CHAT_ID)
        )

        print("✅ Пост успешно опубликован.")
        logging.info("✅ Пост успешно опубликован.")

    except Exception as e:
        logging.error(f"❌ Ошибка при публикации: {e}")
        print(f"❌ Ошибка при публикации: {e}")

if __name__ == "__main__":
    run()
