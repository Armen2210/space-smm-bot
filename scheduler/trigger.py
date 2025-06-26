# scheduler/trigger.py

import os
import sys
import logging
import httpx
from dotenv import load_dotenv
from telegram import Bot
from openai import OpenAI

# === 📂 Добавляем корень проекта в PYTHONPATH ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# ✅ Отладочный вывод
print("✅ trigger.py запущен", flush=True)
logging.basicConfig(level=logging.INFO)
logging.info("✅ trigger.py запущен (логгер работает)")

# === 📦 Импорт после настройки пути ===
from utils.post_utils import send_post_to_telegram

# === 🔐 Загрузка переменных окружения ===
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TARGET_CHAT_ID = os.getenv("TARGET_CHAT_ID")

print(f"🔑 TELEGRAM_TOKEN: {bool(TELEGRAM_TOKEN)}", flush=True)
print(f"🔑 OPENAI_API_KEY: {bool(OPENAI_API_KEY)}", flush=True)
print(f"🔑 TARGET_CHAT_ID: {TARGET_CHAT_ID}", flush=True)

assert TELEGRAM_TOKEN, "⛔ TELEGRAM_TOKEN не задан"
assert OPENAI_API_KEY, "⛔ OPENAI_API_KEY не задан"
assert TARGET_CHAT_ID, "⛔ TARGET_CHAT_ID не задан"

# === 🤖 Инициализация клиентов ===
timeout_config = httpx.Timeout(60.0, connect=10.0)
openai_client = OpenAI(api_key=OPENAI_API_KEY, timeout=timeout_config)
telegram_bot = Bot(token=TELEGRAM_TOKEN)


# === 🚀 Главная функция ===
def run():
    try:
        print("▶️ Вход в функцию run()", flush=True)
        logging.info("▶️ Вход в функцию run()")

        print("📤 Вызов send_post_to_telegram()", flush=True)
        send_post_to_telegram(
            client=openai_client,
            bot=telegram_bot,
            chat_id=int(TARGET_CHAT_ID)
        )

        print("✅ Пост успешно опубликован.", flush=True)
        logging.info("✅ Пост успешно опубликован.")

    except Exception as e:
        print(f"❌ Ошибка при публикации: {e}", flush=True)
        logging.error(f"❌ Ошибка при публикации: {e}")


# === 🟢 Точка входа ===
if __name__ == "__main__":
    run()
