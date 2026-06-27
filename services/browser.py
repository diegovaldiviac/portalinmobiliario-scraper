import os
from contextlib import contextmanager

from playwright.sync_api import ProxySettings, sync_playwright

from services.logger import logger

PROXY_SERVER = os.getenv("PROXY_SERVER")
PROXY_USERNAME = os.getenv("PROXY_USERNAME")
PROXY_PASSWORD = os.getenv("PROXY_PASSWORD")


def _proxy_config() -> ProxySettings | None:
    if not PROXY_SERVER:
        return None
    config: ProxySettings = {"server": PROXY_SERVER}
    if PROXY_USERNAME:
        config["username"] = PROXY_USERNAME
    if PROXY_PASSWORD:
        config["password"] = PROXY_PASSWORD
    return config


@contextmanager
def create_browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled", "--disable-dev-shm-usage", "--disable-dbus", "--disable-gpu"],
            proxy=_proxy_config(),
        )
        ctx = browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            locale="es-CL",
        )
        ctx.add_init_script(
            'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
        )
        page = ctx.new_page()
        page.goto("https://www.portalinmobiliario.com/", wait_until="domcontentloaded", timeout=60000)
        logger.info("Browser initialized")
        yield page
        browser.close()


def fetch_page(page, url):
    page.goto(url, wait_until="domcontentloaded", timeout=90000)
    page.wait_for_selector("li.ui-search-layout__item", timeout=30000)
    return page.content()
