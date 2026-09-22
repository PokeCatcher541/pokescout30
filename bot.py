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

    results = []

    for product in PRODUCTS:
        result = check_product(product)

        if result["page_loaded"]:
            status = f"✅ Page loaded ({result['status_code']})"
        else:
            status = f"❌ Page failed ({result['status_code']})"

        results.append(
            f"🎴 {result['name']}\n"
            f"🏪 {result['store']}\n"
            f"{status}"
        )

    message = (
        "🧪 POKÉSCOUT WEB TEST\n\n"
        + "\n\n".join(results)
        + f"\n\nScan time: {current_time}"
    )

    send_telegram(message)


if __name__ == "__main__":
    main()
