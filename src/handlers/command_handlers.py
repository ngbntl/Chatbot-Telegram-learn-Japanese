from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db_manager import DatabaseManager
from config import DATABASE_PATH

db_manager = DatabaseManager(DATABASE_PATH)

async def start_command(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Thêm từ mới", callback_data="menu_add_word"),
            InlineKeyboardButton(text="🔍 Ôn tập", callback_data="menu_review")
        ],
        [
            InlineKeyboardButton(text="📊 Thống kê", callback_data="menu_stats"),
            InlineKeyboardButton(text="❓ Trợ giúp", callback_data="menu_help")
        ]
    ])
    
    welcome_text = (
        "👋 <b>Chào mừng đến với Bot Từ Vựng Tiếng Nhật!</b>\n\n"
        "Bot này sẽ giúp bạn học và ghi nhớ từ vựng tiếng Nhật với phương pháp ôn tập cách quãng.\n\n"
        "Chọn một trong các tùy chọn bên dưới hoặc gửi tin nhắn theo định dạng:\n"
        "<i>日本語 - nghĩa tiếng Việt</i>"
    )
    
    await message.answer(welcome_text, reply_markup=keyboard)

async def help_command(message: types.Message):
    help_text = (
        "📚 <b>Hướng dẫn sử dụng Bot Từ Vựng Tiếng Nhật</b>\n\n"
        "• Gửi <code>từ tiếng Nhật - nghĩa tiếng Việt</code> để thêm từ mới\n"
        "• Dùng /review để ôn tập các từ đến hạn\n"
        "• Dùng /stats để xem thống kê tiến độ học tập\n"
        "• Dùng /start để hiển thị menu chính\n\n"
        "Ví dụ:\n"
        "→ <code>漢字 - chữ Hán</code>\n"
        "→ <code>勉強する - học tập</code>"
    )
    await message.answer(help_text)

async def review_command(message: types.Message):
    word = db_manager.get_word_for_review()
    
    if not word:
        await message.answer("👏 Hiện không có từ nào cần ôn tập! Hãy quay lại sau nhé.")
        return
    
    word_id, japanese, meaning = word
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👎 Khó", callback_data=f"review_{word_id}_1"),
            InlineKeyboardButton(text="😐 Tạm được", callback_data=f"review_{word_id}_3"),
            InlineKeyboardButton(text="👍 Dễ", callback_data=f"review_{word_id}_5")
        ]
    ])
    
    await message.answer(f"<b>{japanese}</b>\n\nBạn có nhớ từ này không?", reply_markup=keyboard)

async def stats_command(message: types.Message):
    total, due, mastered = db_manager.get_stats()
    
    stats_text = (
        "📊 <b>Thống kê từ vựng của bạn</b>\n\n"
        f"📚 Tổng số từ: {total}\n"
        f"⏰ Từ đến hạn ôn tập: {due}\n"
        f"✅ Từ đã thuộc: {mastered}"
    )
    
    await message.answer(stats_text)

async def process_callback(callback: types.CallbackQuery):
    action = callback.data
    
    if action == "menu_add_word":
        await callback.message.answer("Vui lòng gửi từ tiếng Nhật và nghĩa theo định dạng:\n<code>日本語 - nghĩa tiếng Việt</code>")
    elif action == "menu_review":
        word = db_manager.get_word_for_review()
        if not word:
            await callback.message.answer("👏 Hiện không có từ nào cần ôn tập! Hãy quay lại sau nhé.")
        else:
            word_id, japanese, meaning = word
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Xem nghĩa", callback_data=f"show_meaning_{word_id}")
                ],
                [
                    InlineKeyboardButton(text="👎 Khó", callback_data=f"review_{word_id}_1"),
                    InlineKeyboardButton(text="😐 Tạm được", callback_data=f"review_{word_id}_3"),
                    InlineKeyboardButton(text="👍 Dễ", callback_data=f"review_{word_id}_5")
                ]
            ])
            await callback.message.answer(f"<b>{japanese}</b>\n\nBạn có nhớ từ này không?", reply_markup=keyboard)
    elif action == "menu_stats":
        total, due, mastered = db_manager.get_stats()
        stats_text = (
            "📊 <b>Thống kê từ vựng của bạn</b>\n\n"
            f"📚 Tổng số từ: {total}\n"
            f"⏰ Từ đến hạn ôn tập: {due}\n"
            f"✅ Từ đã thuộc: {mastered}"
        )
        await callback.message.answer(stats_text)
    elif action == "menu_help":
        help_text = (
            "📚 <b>Hướng dẫn sử dụng Bot Từ Vựng Tiếng Nhật</b>\n\n"
            "• Gửi <code>từ tiếng Nhật - nghĩa tiếng Việt</code> để thêm từ mới\n"
            "• Dùng /review để ôn tập các từ đến hạn\n"
            "• Dùng /stats để xem thống kê tiến độ học tập\n"
            "• Dùng /start để hiển thị menu chính\n\n"
            "Ví dụ:\n"
            "→ <code>漢字 - chữ Hán</code>\n"
            "→ <code>勉強する - học tập</code>"
        )
        await callback.message.answer(help_text)
    elif action.startswith("show_meaning_"):
        word_id = int(action.split("_")[2])
        word_info = db_manager.get_word_by_id(word_id)
        if word_info:
            _, japanese, meaning = word_info
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="👎 Khó", callback_data=f"review_{word_id}_1"),
                    InlineKeyboardButton(text="😐 Tạm được", callback_data=f"review_{word_id}_3"),
                    InlineKeyboardButton(text="👍 Dễ", callback_data=f"review_{word_id}_5")
                ]
            ])
            await callback.message.answer(f"<b>{japanese}</b>\n\nNghĩa: {meaning}", reply_markup=keyboard)
    elif action.startswith("review_"):
        parts = action.split("_")
        word_id = int(parts[1])
        performance = int(parts[2])
        
        from datetime import datetime, timedelta
        
        if performance == 1: 
            days_until_review = 1
        elif performance == 3: 
            days_until_review = 3
        else:
            days_until_review = 7
            
        next_review = datetime.now() + timedelta(days=days_until_review)
        rep_count, ease_factor = db_manager.get_word_data(word_id)
        rep_count += 1
        
        db_manager.update_word_review(word_id, rep_count, ease_factor, next_review)
        
        if performance == 1:
            await callback.message.answer("📝 Bạn cần ôn tập từ này thêm. Sẽ hiển thị lại vào ngày mai.")
        elif performance == 3:
            await callback.message.answer("👍 Tốt! Từ này sẽ hiển thị lại sau 3 ngày.")
        else:
            await callback.message.answer("🎉 Tuyệt vời! Bạn đã thuộc từ này. Sẽ hiển thị lại sau 7 ngày.")
            
        next_word = db_manager.get_word_for_review()
        if next_word:
            word_id, japanese, meaning = next_word
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Xem nghĩa", callback_data=f"show_meaning_{word_id}")
                ],
                [
                    InlineKeyboardButton(text="👎 Khó", callback_data=f"review_{word_id}_1"),
                    InlineKeyboardButton(text="😐 Tạm được", callback_data=f"review_{word_id}_3"),
                    InlineKeyboardButton(text="👍 Dễ", callback_data=f"review_{word_id}_5")
                ]
            ])
            await callback.message.answer(f"<b>Từ tiếp theo:</b>\n\n<b>{japanese}</b>\n\nBạn có nhớ từ này không?", reply_markup=keyboard)
    
    await callback.answer()

def register_command_handlers(dp: Dispatcher):
    dp.message.register(start_command, Command(commands=["start"]))
    dp.message.register(help_command, Command(commands=["help"]))
    dp.message.register(review_command, Command(commands=["review"]))
    dp.message.register(stats_command, Command(commands=["stats"]))
    
    dp.callback_query.register(process_callback)