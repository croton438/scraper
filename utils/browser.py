from playwright.async_api import async_playwright
import asyncio

_playwright = None
_browser = None

async def _ensure_playwright():
    global _playwright, _browser
    if not _playwright:
        _playwright = await async_playwright().start()
    if not _browser:
        _browser = await _playwright.chromium.launch(
            headless=False,  # istersen True yap
            args=["--disable-blink-features=AutomationControlled"]
        )

async def new_page():
    await _ensure_playwright()
    context = await _browser.new_context(ignore_https_errors=True)
    page = await context.new_page()
    return page

async def close_page(page):
    try:
        await page.context.close()
    except:
        pass

async def save_cookies(name: str, page):
    cookies = await page.context.cookies()
    with open(f"storage/cookies/{name}.json", "w", encoding="utf-8") as f:
        import json
        json.dump(cookies, f, indent=2, ensure_ascii=False)

async def load_cookies(name: str, page):
    import os, json
    path = f"storage/cookies/{name}.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            cookies = json.load(f)
        await page.context.add_cookies(cookies)
