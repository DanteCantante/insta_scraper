# Working as of 10/21/2024 9PM

import asyncio
import sys
from playwright.async_api import async_playwright
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time


# Proxy URL.
SBR_WS_CDP = "wss://brd-customer-hl_66d0f3ff-zone-scraping_browser1:e9ox96e2cni4@brd.superproxy.io:9222"

# The random UserAgent setup.
ua = UserAgent()
USER_AGENT = ua.random


async def main():
    # Checks to see if the correct amount of command line args are provided.
    result = check_sys_len(sys.argv, 2)

    if result == False:
        sys.exit("Incorrect ammount of command line args")

    print("Connecting to Scraping Browser...")

    async with async_playwright() as playwright:
        # Launches the browser.
        browser = await playwright.chromium.connect_over_cdp(SBR_WS_CDP)

        # Create a new context with custom options.
        context = await browser.new_context(
            user_agent=f"{USER_AGENT}",
            viewport={"width": 1920, "height": 1080},
            java_script_enabled=True,
        )

        # Remove navigator.webdriver property to prevent detection.
        await context.add_init_script(
            """() => {
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        }"""
        )

        try:
            # Opens an empty web browser page.
            page = await context.new_page()

            print(f"Connected! Navigating to https://www.instagram.com/{sys.argv[1]}/")

            await page.goto(
                f"https://www.instagram.com/{sys.argv[1]}/", wait_until="networkidle"
            )

            print(f"Connected to https://www.instagram.com/{sys.argv[1]}/ ... Currently parsing...")

            html = await page.content()

            # This gives time for the html to render.
            time.sleep(5)

            # a Beautiful soup variable is created so that the html can be parsed through.
            soup = BeautifulSoup(html, "html.parser")

            photo_count, followers, following = soup.find_all(
                "span",
                {
                    "class": "html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs"
                },
            )

            # This gives beautiful soup time to parse through the html.
            time.sleep(2)

            # The html content is parsed so that only the value of it remains.
            photo_count = photo_count.text
            followers = followers.text
            following = following.text

            # The strings are converted into integers that can manipulated.
            followers = convert_to_digits_follow(followers)
            following = convert_to_digits_follow(following)
            photo_count = convert_to_digits_photo(photo_count)

            # The results are printed.
            print(f"Followers: {followers}")
            print(f"Following: {following}")
            print(f"Photo count: {photo_count}")

        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            await browser.close()


def check_sys_len(arg, size):
    if len(arg) != size:
        return False
    else:
        return True


def convert_to_digits_photo(arg=str):
    if "M" not in arg and "K" not in arg:
        full_number = ""

        args = arg.split(",")

        for i in args:
            full_number = full_number + i

        full_number = int(full_number)
        return full_number


def convert_to_digits_follow(arg=str):
    if "M" not in arg and "K" not in arg:
        full_number = ""

        args = arg.split(",")

        for i in args:
            full_number = full_number + i

        full_number = int(full_number)
        return full_number

    elif arg.endswith("K"):
        arg = arg.rstrip("K")

        full_number = float(arg)

        return full_number * 1000

    elif arg.endswith("M"):
        arg = arg.rstrip("M")

        full_number = float(arg)

        return full_number * 1000000


if __name__ == "__main__":
    asyncio.run(main())
