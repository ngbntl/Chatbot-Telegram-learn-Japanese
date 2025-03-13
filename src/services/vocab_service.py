from database.db_manager import DatabaseManager
from models.vocabulary import Vocabulary

class VocabService:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def add_word(self, word: str, meaning: str):
        vocab_entry = Vocabulary(word=word, meaning=meaning)
        self.db_manager.insert_word(vocab_entry)

    def get_words_for_review(self):
        return self.db_manager.fetch_words_for_review()

    def update_user_progress(self, user_id: int, word_id: int, progress: str):
        self.db_manager.update_progress(user_id, word_id, progress)