import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from src.app.settings import Settings
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session", autouse=True)
def _load_env():
    # Load .env if present (do not commit .env)
    load_dotenv(ROOT / ".env", override=False)


@pytest.fixture(scope="session")
def settings():
    s = Settings()
    assert s.mx_password, "MX_PASSWORD is empty. Check .env loading."
    return s


@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright, settings):
    browser = playwright.chromium.launch(headless=settings.headless)
    yield browser
    browser.close()


@pytest.fixture
def context(browser):
    ctx = browser.new_context(ignore_https_errors=True)
    yield ctx
    ctx.close()


@pytest.fixture
def page(context):
    p = context.new_page()
    yield p
