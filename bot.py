# bot.py

import logging
import os
from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from openai import OpenAI
from utils.post_utils import send_post_to_telegram_async

# Загружаем переменные из .env
load_dotenv()

# Получаем переменные окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TARGET_CHAT_ID = os.getenv("TARGET_CHAT_ID")

# Проверка на наличие всех переменных
assert TELEGRAM_TOKEN, "⛔ TELEGRAM_TOKEN не задан в .env"
assert OPENAI_API_KEY, "⛔ OPENAI_API_KEY не задан в .env"
assert TARGET_CHAT_ID, "⛔ TARGET_CHAT_ID не задан в .env"

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Инициализация OpenAI и Telegram
openai_client = OpenAI(api_key=OPENAI_API_KEY)
telegram_bot = Bot(token=TELEGRAM_TOKEN)


# Команда /new_post
async def new_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await send_post_to_telegram_async(
            client=openai_client,
            bot=context.bot,
            chat_id=int(TARGET_CHAT_ID)
        )
        await update.message.reply_text("✅ Пост успешно опубликован!")
    except Exception as e:
        logging.error(f"Ошибка при генерации поста: {e}")
        await update.message.reply_text("❌ Ошибка при создании поста.")


# Запуск бота
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("new_post", new_post))
    app.run_polling()


if __name__ == "__main__":
    main()
