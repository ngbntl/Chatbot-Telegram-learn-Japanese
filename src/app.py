import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand, BotCommandScopeDefault
from config import TOKEN, DATABASE_PATH
from database.db_manager import DatabaseManager
from handlers.command_handlers import register_command_handlers
from handlers.vocab_handlers import register_vocab_handlers

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

db_manager = DatabaseManager(DATABASE_PATH)

async def set_commands():
    commands = [
        BotCommand(command="start", description="Bắt đầu/Hiển thị menu chính"),
        BotCommand(command="add", description="Thêm từ vựng mới"),
        BotCommand(command="review", description="Ôn tập từ vựng"),
        BotCommand(command="stats", description="Xem thống kê học tập"),
        BotCommand(command="help", description="Hướng dẫn sử dụng")
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())

@dp.startup()
async def on_startup():
    db_manager.create_tables()
    
    await set_commands()
    
    register_command_handlers(dp)
    register_vocab_handlers(dp)
    
    print("Bot đã khởi động thành công!")

async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())