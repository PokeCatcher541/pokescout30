import os
import requests
from datetime import datetime, timezone

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

    response = requests.post(
        url,
        data=data,
        timeout=20
    )

    response.raise_for_status()


def main():

    current_time = datetime.now(timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )

    print("=" * 50)
    print("POKESCOUT 30")
    print("=" * 50)

    print(f"Products loaded: {len(PRODUCTS)}")
    print(f"Scan started: {current_time}")
    print()

    for product in PRODUCTS:

        result = check_product(product)

        print(
    f"{result['id']} | "
    f"{result['store']} | "
    f"{result['status']} | "
    f"HTTP: {result['status_code']}"
    )

if result.get("error"):
    print(f"  Error: {result['error']}")

    print()
    print("Scan complete.")
    print("No Telegram message sent.")


if __name__ == "__main__":
    main()
