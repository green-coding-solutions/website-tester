import contextlib
import sys
from time import time_ns, sleep

from playwright.sync_api import Playwright, sync_playwright, expect, TimeoutError

proxy_server = {
    "server": "http://squid:3128",
}

def log_note(message: str) -> None:
    timestamp = str(time_ns())[:16]
    print(f"{timestamp} {message}")

def run(playwright: Playwright, browser_name: str, url: str) -> None:
    log_note(f"Launch browser {browser_name}")
    if browser_name == "firefox":
        browser = playwright.firefox.launch(headless=True, proxy=proxy_server)
    else:
        # this leverages new headless mode by Chromium: https://developer.chrome.com/articles/new-headless/
        # The mode is however ~40% slower: https://github.com/microsoft/playwright/issues/21216
        browser = playwright.chromium.launch(headless=False,args=["--headless=new"], proxy=proxy_server)
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()

    try:
        log_note("Opening URL")
        page.goto(url)
        page.wait_for_load_state('load')
        log_note("DOM Content Loaded. Staying Idle for 60 seconds to log animations")
        sleep(60)

    except Exception as e:
        if hasattr(e, 'message'): # only Playwright error class has this member
            log_note(f"Exception occurred: {e.message}")
        log_note("Page content was:")
        log_note(page.content())
        raise e

    # ---------------------
    context.close()
    browser.close()


if __name__ == "__main__":
    if len(sys.argv) > 2:
        browser_name = sys.argv[2].lower()
        if browser_name not in ["chromium", "firefox"]:
            print("Invalid browser name. Please choose either 'chromium' or 'firefox'.")
            sys.exit(1)
    else:
        browser_name = "chromium"

    url = sys.argv[1]

    with sync_playwright() as playwright:
        run(playwright, browser_name, url)
