def format_message(word, meaning):
    return f"Word: {word}\nMeaning: {meaning}"

def validate_input(user_input):
    return bool(user_input.strip())

def extract_word_and_meaning(message):
    parts = message.split(" - ")
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    return None, None

def create_daily_review_message(words):
    if not words:
        return "No words to review today."
    review_message = "Today's words for review:\n"
    for word in words:
        review_message += f"- {word}\n"
    return review_message.strip()