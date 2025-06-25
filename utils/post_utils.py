from openai import OpenAI
from datetime import date
import json
import os
import time
import logging
from telegram import Bot

# 📍 Путь к файлу расписания
SCHEDULE_FILE = os.path.join(os.path.dirname(__file__), "..", "schedule_2025_unique.json")


def get_topic_for_today() -> str:
    """
    Возвращает тему поста по текущей дате из файла расписания.
    Если тема не найдена — выбрасывает RuntimeError.
    """
    today = date.today().isoformat()  # формат '2025-06-25'

    try:
        with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
            schedule = json.load(f)

        for entry in schedule:
            if entry["date"] == today:
                return entry["topic"]

        logging.error(f"⛔ Нет темы для текущей даты: {today}")
        raise RuntimeError("Нет темы в расписании на сегодня.")
    except FileNotFoundError:
        logging.critical(f"⛔ Не найден файл расписания: {SCHEDULE_FILE}")
        raise
    except json.JSONDecodeError as e:
        logging.critical(f"⛔ Ошибка чтения JSON файла: {e}")
        raise


def generate_travel_post(client: OpenAI) -> tuple[str, str]:
    """
    Генерирует текст поста от имени космотуриста на тему текущего дня.
    Возвращает: (текст, тема).
    """
    topic = get_topic_for_today()

    # 📜 Промпт, передаваемый в GPT
    prompt = (
        f"Ты — харизматичный тревел-блогер XXIII века, пишущий серию заметок о межпланетных путешествиях. "
        f"Поделись коротким, захватывающим и вдохновляющим постом для своей подписки в Telegram. "
        f"Локация: {topic}. "
        f"Пиши в жанре научной фантастики, но с реалистичными деталями, как будто путешествия по Солнечной системе — уже обыденность. "
        f"Добавь элементы атмосферы: как выглядит место, какие технологии его обслуживают, какие существа или культуры там обитают, какие уникальные развлечения и достопримечательности есть. "
        f"Используй яркий язык, описывай через чувства (запах, свет, звук, движение), но избегай чрезмерной романтизации. "
        f"До 800 символов. Тон — живой, личный, немного удивлённый, как будто ты действительно только что там побывал."
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": "Ты — профессиональный писатель и тревел-блогер XXIII века. "
                        "Ты создаёшь короткие, яркие посты о межпланетных путешествиях для публики, уставшей от Земли и мечтающей о новых горизонтах. "
                        "Твой стиль — живой, образный, реалистичный. "
                        "Ты описываешь сцены будущего так, будто сам там побывал: ощущаешь свет, ветер, запахи, звуки. "
                        "Ты не выдумываешь магию — ты создаёшь правдоподобную фантастику, в которой ИИ, технологии, экосистемы и архитектура работают как настоящее. "
                        "Избегай шаблонов, романтических клише и чрезмерного пафоса. "
                        "Цель — вдохновить читателя мечтать и представить себя в этом путешествии, как будто это уже возможно."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.95,
        max_tokens=800
    )

    content = response.choices[0].message.content.strip()

    # ⛑ Усечём текст до 800 символов на всякий случай
    return content[:800], topic


def generate_image_url(client: OpenAI, topic: str, retries=2) -> str:
    """
    Генерирует реалистичное изображение по теме поста.
    При сбое — возвращает заглушку (URL).
    """
    image_prompt = (
        f"Ultra-realistic high-resolution photograph of a futuristic tourist destination: {topic}. "
        f"Captured on location in the 23rd century by a professional space photographer using a Nikon Z9 camera with a 50mm lens. "
        f"The scene includes detailed architecture, terrain texture, human activity (tourists in advanced spacewear), "
        f"transparent domes, artificial ecosystems, realistic alien landscapes, and atmospheric haze. "
        f"Natural sunlight or local planetary lighting with real-time shadows, soft reflections on surfaces, lens flares from glass or metals, "
        f"dust particles in the air, surface abrasions, environmental effects like wind, mist, or clouds. "
        f"Photographic color palette, cinematic tone, documentary-style framing (mid-distance, natural angle, depth-of-field). "
        f"Avoid stylized art, no painting, no illustration, no concept art, no CGI or 3D rendering, no surreal elements, no unrealistic symmetry."
    )

    for attempt in range(1, retries + 1):
        try:
            logging.info(f"🖼 Попытка генерации изображения {attempt}...")
            response = client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                size="1024x1024",
                quality="hd",
                n=1
            )
            return response.data[0].url
        except Exception as e:
            logging.warning(f"⛔ Генерация изображения не удалась (попытка {attempt}): {e}")
            if attempt < retries:
                time.sleep(5)
            else:
                logging.error("❌ Все попытки генерации изображения не удались.")
                return "https://dummyimage.com/1024x1024/000/fff&text=No+Image+Available"


# === 📦 СИНХРОННАЯ ВЕРСИЯ (используется в trigger.py) ===
def send_post_to_telegram(client: OpenAI, bot: Bot, chat_id: int) -> None:
    """
    Синхронная публикация поста в Telegram.
    Используется в скриптах без async, например trigger.py.
    """
    try:
        text, topic = generate_travel_post(client)
        image_url = generate_image_url(client, topic)

        message = f"<b>{topic}</b>\n\n{text}"

        bot.send_photo(
            chat_id=chat_id,
            photo=image_url,
            caption=message,
            parse_mode='HTML'
        )

        logging.info(f"✅ Пост успешно опубликован: {topic}")
    except Exception as e:
        logging.error(f"❌ Ошибка при публикации поста в Telegram (sync): {e}")
        raise


# === ⚡ АСИНХРОННАЯ ВЕРСИЯ (используется в bot.py) ===
async def send_post_to_telegram_async(client: OpenAI, bot: Bot, chat_id: int) -> None:
    """
    Асинхронная публикация поста в Telegram.
    Используется в асинхронных контекстах, например Telegram-боте.
    """
    try:
        text, topic = generate_travel_post(client)
        image_url = generate_image_url(client, topic)

        message = f"<b>{topic}</b>\n\n{text}"

        await bot.send_photo(
            chat_id=chat_id,
            photo=image_url,
            caption=message,
            parse_mode='HTML'
        )

        logging.info(f"✅ Пост успешно опубликован: {topic}")
    except Exception as e:
        logging.error(f"❌ Ошибка при публикации поста в Telegram (async): {e}")
        raise
