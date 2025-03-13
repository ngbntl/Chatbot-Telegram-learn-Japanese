from datetime import datetime, timedelta
import sqlite3
import asyncio

class ReviewScheduler:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_words_for_review(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT word, meaning FROM words WHERE review_date <= ?", (datetime.now(),))
        words = cur.fetchall()
        conn.close()
        return words

    def update_review_date(self, word):
        next_review_date = datetime.now() + timedelta(days=1)
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("UPDATE words SET review_date = ? WHERE word = ?", (next_review_date, word))
        conn.commit()
        conn.close()

    async def schedule_reviews(self, bot, chat_id):
        while True:
            words = self.get_words_for_review()
            if words:
                for word, meaning in words:
                    await bot.send_message(chat_id, f"Review this word: {word} - {meaning}")
                    self.update_review_date(word)
            await asyncio.sleep(86400) 