# Japanese Vocabulary Bot

This project is a Telegram bot designed to help users learn and retain Japanese vocabulary. Users can add new words, and the bot will remind them to review old words daily for better retention.

## Features

- Add Japanese vocabulary with meanings.
- Daily reminders for vocabulary review.
- User-friendly interface through Telegram.

## Project Structure

```
japanese-vocab-bot
├── src
│   ├── app.py                # Entry point of the application
│   ├── config.py             # Configuration settings for the bot
│   ├── database              # Database management
│   │   ├── __init__.py
│   │   └── db_manager.py
│   ├── handlers              # Command and vocabulary handlers
│   │   ├── __init__.py
│   │   ├── command_handlers.py
│   │   └── vocab_handlers.py
│   ├── models                # Data models
│   │   ├── __init__.py
│   │   └── vocabulary.py
│   ├── services              # Business logic and services
│   │   ├── __init__.py
│   │   ├── review_scheduler.py
│   │   └── vocab_service.py
│   └── utils                 # Utility functions
│       ├── __init__.py
│       └── helpers.py
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd japanese-vocab-bot
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your Telegram bot token in `src/config.py`.

4. Run the bot:
   ```
   python src/app.py
   ```

## Usage

- Start the bot by sending the `/start` command.
- Send a Japanese word to save it in the vocabulary database.
- The bot will remind you to review your saved words daily.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License.