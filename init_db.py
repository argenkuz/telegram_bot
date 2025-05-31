# init_db.py
import asyncio
from database.db import init_db

if __name__ == "__main__":
    asyncio.run(init_db())
    print("✅ База данных успешно создана.")
