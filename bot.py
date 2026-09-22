import os
import requests
from datetime import datetime


TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def send_telegram(message):

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    response = requests.post(url, data=data)

    response.raise_for_status()


def main():

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = f"""
🤖 POKÉSCOUT 30

✅ Bot is alive!

The Pokémon card scout successfully connected to Telegram.

Time:
{current_time}

Next step:
We'll start teaching it how to check Pokémon card products.
"""

    send_telegram(message)


if __name__ == "__main__":
    main()
