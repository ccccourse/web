from playwright.sync_api import sync_playwright

import time

def test_frontend_with_backend(test_server):  # 確保伺服器已啟動
    with sync_playwright() as p:
        # 啟動瀏覽器（無頭模式）
        # browser = p.chromium.launch(headless=True)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 訪問 FastAPI 提供的前端頁面
        page.goto("http://127.0.0.1:8000/")

        # 驗證頁面標題
        assert page.title() == "Playwright Test"
        time.sleep(2)

        # 模擬按鈕點擊並驗證結果
        page.click("button")
        page.wait_for_selector("#output")
        output_text = page.text_content("#output")
        print(f"output_text={output_text}")
        time.sleep(2)
        assert output_text == "Hello from API"

        browser.close()
