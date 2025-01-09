import pytest
from playwright.sync_api import sync_playwright

@pytest.mark.parametrize("browser_type", ["chromium", "firefox", "webkit"])
def test_frontend_with_backend(test_server, browser_type):
    with sync_playwright() as p:
        browser = getattr(p, browser_type).launch(headless=True)
        page = browser.new_page()
        page.goto("http://127.0.0.1:8000/")
        page.click("button")
        page.wait_for_selector("#output")
        assert page.text_content("#output") == "Hello from API"
        browser.close()
