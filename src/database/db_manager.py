import sqlite3
from datetime import datetime, timedelta

class DatabaseManager:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cur = self.conn.cursor()
    
    def create_tables(self):
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY,
            word TEXT,
            meaning TEXT,
            last_reviewed TIMESTAMP,
            next_review TIMESTAMP,
            repetition_count INTEGER DEFAULT 0,
            ease_factor REAL DEFAULT 2.5
        )
        """)
        self.conn.commit()
    
    def add_word(self, word, meaning):
        now = datetime.now()
        next_review = now + timedelta(minutes=10)
        
        self.cur.execute(
            "INSERT INTO words (word, meaning, last_reviewed, next_review, repetition_count) VALUES (?, ?, ?, ?, ?)",
            (word, meaning, now, next_review, 0)
        )
        self.conn.commit()
        return True
    
    def get_word_for_review(self):
        now = datetime.now()
        self.cur.execute("SELECT id, word, meaning FROM words WHERE next_review <= ? ORDER BY next_review LIMIT 1", (now,))
        return self.cur.fetchone()
    
    def get_word_data(self, word_id):
        self.cur.execute("SELECT repetition_count, ease_factor FROM words WHERE id = ?", (word_id,))
        return self.cur.fetchone()
    
    def update_word_review(self, word_id, repetition_count, ease_factor, next_review):
        self.cur.execute(
            "UPDATE words SET repetition_count = ?, ease_factor = ?, last_reviewed = ?, next_review = ? WHERE id = ?",
            (repetition_count, ease_factor, datetime.now(), next_review, word_id)
        )
        self.conn.commit()
    
    def get_stats(self):
        now = datetime.now()
        
        self.cur.execute("SELECT COUNT(*) FROM words")
        total = self.cur.fetchone()[0]
        
        self.cur.execute("SELECT COUNT(*) FROM words WHERE next_review <= ?", (now,))
        due = self.cur.fetchone()[0]
        
        self.cur.execute("SELECT COUNT(*) FROM words WHERE repetition_count >= 5")
        mastered = self.cur.fetchone()[0]
        
        return total, due, mastered
    
        
    def get_word_by_id(self, word_id):
        self.cur.execute("SELECT id, word, meaning FROM words WHERE id = ?", (word_id,))
        return self.cur.fetchone()