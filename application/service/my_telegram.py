import os
import telegram
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")


def send_message(text: str):
    try:
        bot = telegram.Bot(token=token)
        bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        print(f"Error in sending message to Telegram: {e}")
        return None
