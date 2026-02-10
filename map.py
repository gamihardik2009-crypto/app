from playwright.sync_api import sync_playwright

# -------- USER INPUT --------
SEARCH_QUERY = input("Enter what you want to search: ")
LIMIT = int(input("Enter how many results you want: "))
print("wait.........")


def safe_text(page, selector):
    loc = page.locator(selector)
    return loc.inner_text().strip() if loc.count() else ""


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        context = browser.new_context(
            viewport={"width": 1920, "height": 1080}
        )

        # Block heavy assets (speed boost)
        context.route(
            "**/*",
            lambda route, request: (
                route.abort()
                if request.resource_type in ["image", "media", "font"]
                else route.continue_()
            )
        )

        page = context.new_page()
        page.goto("https://www.google.com/maps", timeout=60000)

        # Search
        page.fill('input[name="q"]', SEARCH_QUERY)
        page.keyboard.press("Enter")

        # Wait for results feed (no sleep)
        page.wait_for_selector('div[role="feed"]', timeout=15000)

        results = []
        visited_urls = set()

        while len(results) < LIMIT:
            cards = page.locator("a.hfpxzc")
            count = cards.count()

            for i in range(count):
                if len(results) >= LIMIT:
                    break

                card = cards.nth(i)
                url = card.get_attribute("href")

                if not url or url in visited_urls:
                    continue

                visited_urls.add(url)
                card.click()

                # Wait only for title (fast)
                page.wait_for_selector("h1.DUwDvf", timeout=8000)

                data = {
                    "name": safe_text(page, "h1.DUwDvf"),
                    "address": safe_text(page, 'button[data-item-id="address"] div.Io6YTe'),
                    "phone": safe_text(page, 'button[data-item-id^="phone"] div.Io6YTe'),
                    "category": safe_text(page, 'button[jsaction*="pane.rating.category"]'),
                    "website": (
                        page.locator('a[data-item-id="authority"]').get_attribute("href")
                        if page.locator('a[data-item-id="authority"]').count()
                        else ""
                    ),
                    "url": url
                }

                results.append(data)

                print(f"\n[{len(results)}]")
                for k, v in data.items():
                    print(f"{k.capitalize():9}: {v}")

            # Scroll to load more results (minimal delay)
            page.eval_on_selector(
                'div[role="feed"]',
                "el => el.scrollTop = el.scrollHeight"
            )
            page.wait_for_timeout(1000)  # 1s only

        browser.close()


if __name__ == "__main__":
    run()

