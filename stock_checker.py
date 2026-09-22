import requests


def check_product(product):

    # Product disabled
    if not product.get("enabled", True):
        return {
            "id": product["id"],
            "name": product["name"],
            "store": product["store"],
            "status": "disabled",
            "status_code": None
        }

    # We don't have a verified product URL yet
    if not product.get("url"):
        return {
            "id": product["id"],
            "name": product["name"],
            "store": product["store"],
            "status": "no_url",
            "status_code": None
        }

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/140.0 Safari/537.36"
        )
    }

    try:

        response = requests.get(
            product["url"],
            headers=headers,
            timeout=20
        )

        if response.status_code == 403:
            status = "blocked"

        elif response.status_code == 429:
            status = "rate_limited"

        elif response.ok:
            status = "page_loaded"

        else:
            status = "page_error"

        return {
            "id": product["id"],
            "name": product["name"],
            "store": product["store"],
            "status": status,
            "status_code": response.status_code
        }

    except requests.RequestException as error:

        return {
            "id": product["id"],
            "name": product["name"],
            "store": product["store"],
            "status": "connection_error",
            "status_code": None,
            "error": str(error)
        }
