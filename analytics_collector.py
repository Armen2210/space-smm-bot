import json
import os
from telethon import TelegramClient
from dotenv import load_dotenv

# Загружаем .env
load_dotenv()

# Конфигурация из .env
API_ID = int(os.getenv("TELETHON_API_ID"))
API_HASH = os.getenv("TELETHON_API_HASH")
TARGET_CHAT_ID = os.getenv("TARGET_CHAT_ID")

# Путь к файлам
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MESSAGES_LOG = os.path.join(BASE_DIR, "messages_log.json")
ANALYTICS_LOG = os.path.join(BASE_DIR, "analytics_log.json")

# Инициализация клиента
client = TelegramClient("analytics_session", API_ID, API_HASH)


async def collect_analytics():
    # Загружаем список сообщений
    if not os.path.exists(MESSAGES_LOG):
        print("⛔ messages_log.json не найден")
        return

    with open(MESSAGES_LOG, "r", encoding="utf-8") as f:
        messages = json.load(f)

    analytics_data = []

    for item in messages:
        message_id = item["message_id"]
        topic = item["topic"]
        date = item["date"]

        try:
            # Получаем сообщение
            msg = await client.get_messages(int(TARGET_CHAT_ID), ids=message_id)

            views = msg.views or 0
            replies = msg.replies.replies if msg.replies else 0

            analytics_data.append({
                "message_id": message_id,
                "topic": topic,
                "date": date,
                "views": views,
                "comments": replies
            })

            print(f"✅ {topic}: просмотры={views}, комментарии={replies}")

        except Exception as e:
            print(f"❌ Ошибка при получении данных для message_id={message_id}: {e}")

    # Сохраняем файл
    with open(ANALYTICS_LOG, "w", encoding="utf-8") as f:
        json.dump(analytics_data, f, ensure_ascii=False, indent=2)

    print("✅ Данные сохранены в analytics_log.json")


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(collect_analytics())
