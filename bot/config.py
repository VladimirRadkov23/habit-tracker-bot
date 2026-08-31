import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

if not BOT_TOKEN:
    raise ValueError("Переменная BOT_TOKEN не найдена! Проверь файл .env")
