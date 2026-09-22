import os
import requests
from datetime import datetime, timezone

from products import PRODUCTS
from browser_checker import check_with_browser


TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def send_telegram(message):

    url = (
        f"https://api.telegram.org/"
        f"bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    )

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

    print("=" * 60)
    print("POKESCOUT 30 - BROWSER TEST")
    print("=" * 60)

    print(f"Products loaded: {len(PRODUCTS)}")
    print(f"Scan started: {current_time}")
    print()

    tested = 0

    for product in PRODUCTS:

        if product.get("checker") != "best_buy":
            continue

        tested += 1

        print(f"Testing: {product['name']}")
        print(f"Store: {product['store']}")

        result = check_with_browser(product)

        print(f"Status: {result['status']}")
        print(f"HTTP: {result['http_status']}")
        print(f"Title: {result['title']}")
        print(f"Final URL: {result['final_url']}")

        print(
            "Add to Cart text: "
            f"{result['has_add_to_cart']}"
        )

        print(
            "Sold Out text: "
            f"{result['has_sold_out']}"
        )

        print(
            "Unavailable text: "
            f"{result['has_unavailable']}"
        )

        if result.get("error"):
            print(f"Error: {result['error']}")

        print("-" * 60)

    print()
    print(f"Browser products tested: {tested}")
    print("Browser test complete.")
    print("No Telegram alert sent.")


if __name__ == "__main__":
    main()
