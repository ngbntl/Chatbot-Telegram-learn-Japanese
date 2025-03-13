import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("Không tìm thấy TELEGRAM_TOKEN trong biến môi trường hoặc file .env")

DATABASE_PATH = os.environ.get("DATABASE_PATH", "vocab.db")