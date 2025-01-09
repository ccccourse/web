from playwright.sync_api import sync_playwright

import time

def test_frontend_with_backend(test_server):  # 確保伺服器已啟動
    with sync_playwright() as p:
        # 啟動瀏覽器（無頭模式）
        # browser = p.chromium.launch(headless=True)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print('enter home page ...')
        # 訪問 FastAPI 提供的前端頁面
        page.goto("http://127.0.0.1:8000/")
        time.sleep(2)

        # 驗證頁面標題
        html = page.content()
        print('we should have 0 post at start')
        assert '<p>You have <strong>0</strong> posts!</p>' in html

        print('create post: ')
        page.click('#createPost')
        time.sleep(2)
        html = page.content()
        assert '<h1>New Post</h1>' in html

        print('key in : title=aaa, body=aaa')
        page.focus('#title')
        page.keyboard.type('aaa')
        page.focus('#body')
        page.keyboard.type('aaa')
        page.click('#savePost')

        time.sleep(2)
        html = page.content()
        print('we should have 1 post now...')
        assert '<p>You have <strong>1</strong> posts!</p>' in html

        page.click('#show0')
        time.sleep(2)
        html = page.content()
        print('the title of posts[0] is aaa')
        assert '<h1>aaa</h1>' in html

        browser.close()


"""
# 模擬按鈕點擊並驗證結果
page.click("button")
page.wait_for_selector("#output")
output_text = page.text_content("#output")
print(f"output_text={output_text}")
time.sleep(2)
assert output_text == "Hello from API"
"""

"""

Deno.test('Puppteer', async function() {
  browser = await puppeteer.launch(opts);
  page = await browser.newPage();

  var html;

  await page.goto('http://127.0.0.1:8000', {waitUntil: 'domcontentloaded'})
  await sleep(500);
  html = await page.content()
  console.log('html=', html)
  let idx = html.indexOf('<p>You have <strong>0</strong> posts!</p>')
  console.log('idx=', idx)
  ok(idx >= 0)

  // console.log('test create post...')
  await page.click('#createPost')
  await sleep(500);
  html = await page.content()
  ok(html.indexOf('<h1>New Post</h1>') >= 0)

  // console.log('test add post...')
  await page.focus('#title')
  await page.keyboard.type('aaa')
  await page.focus('#body')
  await page.keyboard.type('aaa')
  await page.click('#savePost')

  // console.log('we should have 1 post now...')
  await sleep(500);
  html = await page.content()
  ok(html.indexOf('<p>You have <strong>1</strong> posts!</p>') >= 0)

  await page.click('#show0')
  await sleep(500);
  html = await page.content()
  ok(html.indexOf('<h1>aaa</h1>') >= 0)
  await browser.close();
})
"""