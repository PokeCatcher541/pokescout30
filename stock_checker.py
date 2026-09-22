import requests


def check_product(product):
    """
    Checks a product webpage and returns information about the request.

    This is our first test version.
    It does NOT decide whether something is actually in stock yet.
    """

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

        return {
            "name": product["name"],
            "store": product["store"],
            "url": product["url"],
            "status_code": response.status_code,
            "page_loaded": response.ok,
            "html": response.text
        }

    except requests.RequestException as error:
        return {
            "name": product["name"],
            "store": product["store"],
            "url": product["url"],
            "status_code": None,
            "page_loaded": False,
            "html": "",
            "error": str(error)
        }
