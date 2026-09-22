import os
import requests
from datetime import datetime

from products import PRODUCTS
from stock_checker import check_product

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "disable_web_page_preview": True
    }

    response = requests.post(url, data=data, timeout=20)
    response.raise_for_status()


def main():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("Starting PokéScout 30...")
    print(f"Products loaded: {len(PRODUCTS)}")
    print(f"Scan time: {current_time}")

    for product in PRODUCTS:
        result = check_product(product)

        print(
            f"{result['name']} | "
            f"{result['store']} | "
            f"HTTP {result['status_code']}"
        )

    print("Scan complete.")
    print("Telegram alerts are currently disabled while stock detection is being built.")


if __name__ == "__main__":
    main()
