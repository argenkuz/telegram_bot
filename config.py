from dotenv import load_dotenv
import os

load_dotenv()  # Загружаем .env

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = "sqlite+aiosqlite:///database/data.sqlite"
