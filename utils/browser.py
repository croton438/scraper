"""
Playwright browser yönetimi
"""
from playwright.async_api import async_playwright, Page

_playwright = None
_browser = None
_context = None


async def new_page() -> Page:
    global _playwright, _browser, _context
    if _playwright is None:
        _playwright = await async_playwright().start()
    if _browser is None:
        _browser = await _playwright.chromium.launch(
            headless=False,  # Windows VDS olduğu için pencereyi açar
            slow_mo=200
        )
    if _context is None:
        _context = await _browser.new_context(viewport={"width": 1600, "height": 900})
    return await _context.new_page()


async def close_page(page: Page):
    if page and not page.is_closed():
        await page.close()


async def close_browser():
    global _playwright, _browser, _context
    if _context:
        await _context.close()
        _context = None
    if _browser:
        await _browser.close()
        _browser = None
    if _playwright:
        await _playwright.stop()
        _playwright = None
