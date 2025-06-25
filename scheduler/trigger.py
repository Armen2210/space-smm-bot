# scheduler/trigger.py

import os
import logging
from dotenv import load_dotenv
from telegram import Bot
from openai import OpenAI
from utils.post_utils import send_post_to_telegram
import httpx

# Загрузка переменных окружения
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TARGET_CHAT_ID = os.getenv("TARGET_CHAT_ID")

# Проверка наличия всех переменных
assert TELEGRAM_TOKEN, "⛔ TELEGRAM_TOKEN не задан в .env"
assert OPENAI_API_KEY, "⛔ OPENAI_API_KEY не задан в .env"
assert TARGET_CHAT_ID, "⛔ TARGET_CHAT_ID не задан в .env"

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Настройка клиента OpenAI с таймаутом
timeout_config = httpx.Timeout(60.0, connect=10.0)
openai_client = OpenAI(api_key=OPENAI_API_KEY, timeout=timeout_config)

# Telegram bot
telegram_bot = Bot(token=TELEGRAM_TOKEN)


def run():
    try:
        send_post_to_telegram(
            client=openai_client,
            bot=telegram_bot,
            chat_id=int(TARGET_CHAT_ID)
        )
        print("✅ Пост успешно опубликован.")
    except Exception as e:
        logging.error(f"❌ Ошибка при публикации: {e}")
        print("❌ Ошибка при публикации.")


if __name__ == "__main__":
    run()
