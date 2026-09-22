from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def check_with_browser(product):

    result = {
        "id": product["id"],
        "name": product["name"],
        "store": product["store"],
        "url": product.get("url"),
        "status": "unknown",
        "http_status": None,
        "title": None,
        "final_url": None,
        "has_add_to_cart": False,
        "has_sold_out": False,
        "has_unavailable": False,
        "error": None
    }

    if not product.get("enabled", True):
        result["status"] = "disabled"
        return result

    if not product.get("url"):
        result["status"] = "no_url"
        return result

    try:

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True
            )

            page = browser.new_page(
                viewport={
                    "width": 1280,
                    "height": 900
                }
            )

            response = page.goto(
                product["url"],
                wait_until="domcontentloaded",
                timeout=30000
            )

            if response:
                result["http_status"] = response.status

            result["final_url"] = page.url
            result["title"] = page.title()

            # Give client-side JavaScript a short opportunity
            # to render product controls.
            page.wait_for_timeout(3000)

            body_text = page.locator("body").inner_text(
                timeout=10000
            )

            body_lower = body_text.lower()

            result["has_add_to_cart"] = (
                "add to cart" in body_lower
            )

            result["has_sold_out"] = (
                "sold out" in body_lower
            )

            result["has_unavailable"] = (
                "unavailable" in body_lower
                or "not available" in body_lower
            )

            # IMPORTANT:
            # This is diagnostic only.
            # We are NOT declaring inventory yet.

            if result["http_status"] == 403:
                result["status"] = "blocked"

            elif result["http_status"] == 429:
                result["status"] = "rate_limited"

            elif result["http_status"] and result["http_status"] >= 400:
                result["status"] = "page_error"

            else:
                result["status"] = "browser_loaded"

            browser.close()

    except PlaywrightTimeoutError as error:

        result["status"] = "timeout"
        result["error"] = str(error)

    except Exception as error:

        result["status"] = "browser_error"
        result["error"] = str(error)

    return result
