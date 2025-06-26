# scheduler/server.py
import os
import sys
import logging
import asyncio
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import httpx

# === 📂 Добавляем корень проекта в PYTHONPATH ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from telegram import Bot
from openai import OpenAI
from utils.post_utils import send_post_to_telegram_async  # ⚠️ исправлено

# Загрузка .env
load_dotenv()

# Настройка логов
logging.basicConfig(level=logging.INFO)

# Инициализация Flask
app = Flask(__name__)

# Конфигурация переменных
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TARGET_CHAT_ID = os.getenv("TARGET_CHAT_ID")
PUBLISH_SECRET = os.getenv("PUBLISH_SECRET")

# Проверка
assert TELEGRAM_TOKEN, "⛔ TELEGRAM_TOKEN не задан"
assert OPENAI_API_KEY, "⛔ OPENAI_API_KEY не задан"
assert TARGET_CHAT_ID, "⛔ TARGET_CHAT_ID не задан"
assert PUBLISH_SECRET, "⛔ PUBLISH_SECRET не задан"

# Инициализация клиентов
timeout_config = httpx.Timeout(60.0, connect=10.0)
openai_client = OpenAI(api_key=OPENAI_API_KEY, timeout=timeout_config)
telegram_bot = Bot(token=TELEGRAM_TOKEN)

@app.route('/publish', methods=['POST'])
def publish_post():
    # === 🔒 Проверка заголовка безопасности ===
    token = request.headers.get("X-Auth-Token")
    if token != PUBLISH_SECRET:
        logging.warning("⛔ Неавторизованный запрос на публикацию")
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    try:
        logging.info(f"📥 Получен запрос от IP: {request.remote_addr}")

        # ✅ Асинхронный вызов
        asyncio.run(send_post_to_telegram_async(
            client=openai_client,
            bot=telegram_bot,
            chat_id=int(TARGET_CHAT_ID)
        ))

        logging.info("✅ Пост успешно опубликован.")
        return jsonify({"status": "ok", "message": "Пост опубликован"}), 200

    except Exception as e:
        logging.error(f"❌ Ошибка при публикации: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return "🚀 Сервер работает!", 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
