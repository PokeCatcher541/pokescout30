import os
import requests
from datetime import datetime

from products import PRODUCTS

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


def build_product_list():
    lines = []

    for product in PRODUCTS:
        lines.append(
            f"🎴 {product['name']}\n"
            f"🏪 {product['store']}\n"
            f"📦 {product['category']}\n"
            f"🔗 {product['url']}"
        )

    return "\n\n".join(lines)


def main():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    product_list = build_product_list()

    message = (
        "🤖 POKÉSCOUT 30\n\n"
        "✅ Product database loaded successfully!\n\n"
        f"{product_list}\n\n"
        f"Products loaded: {len(PRODUCTS)}\n\n"
        f"Scan time: {current_time}"
    )

    send_telegram(message)


if __name__ == "__main__":
    main()
