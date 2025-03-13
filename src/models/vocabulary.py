from datetime import datetime
from datetime import datetime, timedelta

class Vocabulary:
    def __init__(self, word: str, meaning: str, review_schedule: str = None):
        self.word = word
        self.meaning = meaning
        self.review_schedule = review_schedule or self.set_review_schedule()

    def set_review_schedule(self):
        return (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    def to_dict(self):
        return {
            "word": self.word,
            "meaning": self.meaning,
            "review_schedule": self.review_schedule
        }