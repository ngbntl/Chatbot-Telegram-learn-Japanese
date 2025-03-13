from aiogram import Dispatcher, types
from utils.helpers import extract_word_and_meaning
from database.db_manager import DatabaseManager
from config import DATABASE_PATH
import requests
import re

db_manager = DatabaseManager(DATABASE_PATH)

async def save_word(message: types.Message):
    word, meaning = extract_word_and_meaning(message.text)
    
    if word and meaning:
        db_manager.add_word(word, meaning)
        await message.reply(f"✅ Đã lưu từ: <b>{word}</b>\nNghĩa: {meaning}")
    else:
        await message.reply("❌ Vui lòng sử dụng định dạng: <b>từ tiếng Nhật - nghĩa tiếng Việt</b>")

def register_vocab_handlers(dp: Dispatcher):
    dp.message.register(save_word, lambda msg: not msg.text.startswith('/'))

def extract_word_and_meaning(text):
    """
    Extract Japanese word and meaning from text in format "word - meaning"
    Returns a tuple of (word, meaning) or (None, None) if format is incorrect
    """
    match = re.match(r'^(.*?)\s*-\s*(.*)$', text)
    if match:
        word = match.group(1).strip()
        meaning = match.group(2).strip()
        return word, meaning
    return None, None