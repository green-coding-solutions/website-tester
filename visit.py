import contextlib
import sys
from time import time_ns, sleep
import os
import argparse

from playwright.sync_api import Playwright, sync_playwright, expect, TimeoutError

proxy_server = {
    "server": "http://squid:3128",
}

def log_note(message: str) -> None:
    timestamp = str(time_ns())[:16]
    print(f"{timestamp} {message}")

def run(playwright: Playwright, browser_name: str, fifo_path = str) -> None:
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
        for i in range(1,10):
            with open(fifo_path, 'r') as fifo:
              # Read data from the named pipe
              url = fifo.read()
              log_note(f"Opening URL {url}")
              context = browser.new_context(ignore_https_errors=True)
              page = context.new_page()
              page.goto(url)
              page.wait_for_load_state('load')
              log_note(f"Finished loading URL {url}")


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
    parser = argparse.ArgumentParser()
    parser.add_argument('--browser', type=str, help='Select Firefox or Chromium', default='chromium')
    parser.add_argument('--fifo-path', type=str, help='Specify the path to the FIFO buffer to use for going to next page', default='/tmp/my_fifo')
    args = parser.parse_args()

    with sync_playwright() as playwright:
        run(playwright, browser=args.browser.lower(), fifo_path=args.fifo_path)
