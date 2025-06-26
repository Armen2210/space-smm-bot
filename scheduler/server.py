# scheduler/server.py

import os
import subprocess
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Загрузка .env
load_dotenv()

# Настройка логов
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/publish', methods=['POST'])
def publish_post():
    try:
        logging.info(f"📥 Получен запрос на публикацию от IP: {request.remote_addr}")
        # 👇 Передаём переменные окружения в subprocess
        env = os.environ.copy()

        result = subprocess.run(
            ["python3", os.path.join(os.path.dirname(__file__), "trigger.py")],
            check=True,
            timeout=60,
            capture_output=True,
            text=True,
            env=env  # 👈 передаём переменные окружения дочернему процессу
        )
        logging.info(f"📤 Результат запуска: {result.stdout.strip()}")
        return jsonify({"status": "ok", "message": "Пост опубликован"}), 200

    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Ошибка при запуске trigger.py: {e.stderr.strip()}")
        return jsonify({"status": "error", "message": str(e.stderr)}), 500

    except subprocess.TimeoutExpired:
        logging.error("⏱ Таймаут выполнения trigger.py")
        return jsonify({"status": "error", "message": "Timeout при запуске trigger.py"}), 504

@app.route('/', methods=['GET'])
def home():
    return "🚀 Сервер работает!", 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)