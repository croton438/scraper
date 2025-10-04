"""
Playwright browser yönetimi - Sync fonksiyonlar
"""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

_playwright = None
_browser = None
_context = None


def new_page():
    """
    Yeni bir sayfa açar
    """
    global _playwright, _browser, _context

    if _playwright is None:
        _playwright = sync_playwright().start()

    if _browser is None:
        _browser = _playwright.chromium.launch(
            headless=False,  # Debug için False, sunucuda True yapılabilir
            args=["--disable-blink-features=AutomationControlled"]
        )

    if _context is None:
        _context = _browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        )

    return _context.new_page()


def close_browser():
    global _playwright, _browser, _context
    if _context:
        _context.close()
        _context = None
    if _browser:
        _browser.close()
        _browser = None
    if _playwright:
        _playwright.stop()
        _playwright = None


def save_cookies(company_name: str):
    global _context
    if not _context:
        return
    cookies_dir = Path("storage/cookies")
    cookies_dir.mkdir(parents=True, exist_ok=True)
    cookie_file = cookies_dir / f"{company_name}.json"
    cookies = _context.cookies()
    with open(cookie_file, "w", encoding="utf-8") as f:
        json.dump(cookies, f, indent=2, ensure_ascii=False)
    print(f"✓ Çerezler kaydedildi: {cookie_file}")


def load_cookies(company_name: str) -> bool:
    global _context
    if not _context:
        return False
    cookie_file = Path("storage/cookies") / f"{company_name}.json"
    if not cookie_file.exists():
        return False
    try:
        with open(cookie_file, "r", encoding="utf-8") as f:
            cookies = json.load(f)
        _context.add_cookies(cookies)
        print(f"✓ Çerezler yüklendi: {cookie_file}")
        return True
    except Exception as e:
        print(f"✗ Çerez yükleme hatası: {e}")
        return False
