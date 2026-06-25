import os
from contextlib import contextmanager

from playwright.sync_api import sync_playwright

from services.logger import logger

CHROMIUM_EXECUTABLE = os.getenv("CHROMIUM_EXECUTABLE")


@contextmanager
def create_browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            executable_path=CHROMIUM_EXECUTABLE,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled", "--disable-dev-shm-usage"],
        )
        ctx = browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            locale="es-CL",
        )
        ctx.add_init_script(
            'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
        )
        page = ctx.new_page()
        page.goto("https://www.portalinmobiliario.com/", wait_until="networkidle", timeout=30000)
        logger.info("Browser initialized")
        yield page
        browser.close()


def fetch_page(page, url):
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_selector("li.ui-search-layout__item", timeout=15000)
    return page.content()
