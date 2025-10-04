"""
Playwright browser yönetimi - Async fonksiyonlar
"""
import json
import os
from pathlib import Path
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

# Global playwright instance
_playwright = None
_browser = None
_context = None


async def new_page() -> Page:
    """
    Yeni bir sayfa oluşturur ve döndürür
    
    Returns:
        Page: Playwright page nesnesi
    """
    global _playwright, _browser, _context
    
    if _playwright is None:
        _playwright = await async_playwright().start()
    
    if _browser is None:
        _browser = await _playwright.chromium.launch(
            headless=True,  # Sunucuda headless=True olmalı
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
    
    if _context is None:
        _context = await _browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
    
    page = await _context.new_page()
    return page


async def close_page(page: Page):
    """
    Verilen sayfayı kapatır
    
    Args:
        page: Kapatılacak sayfa
    """
    if page and not page.is_closed():
        await page.close()


async def close_browser():
    """
    Browser ve playwright'i tamamen kapatır
    """
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


async def save_cookies(company_name: str):
    """
    Mevcut context'teki çerezleri kaydeder
    
    Args:
        company_name: Şirket adı (dosya adı için)
    """
    global _context
    
    if _context is None:
        print("⚠ Context bulunamadı, çerezler kaydedilemedi")
        return
    
    cookies_dir = Path("storage/cookies")
    cookies_dir.mkdir(parents=True, exist_ok=True)
    
    cookies = await _context.cookies()
    cookie_file = cookies_dir / f"{company_name}.json"
    
    with open(cookie_file, 'w', encoding='utf-8') as f:
        json.dump(cookies, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Çerezler kaydedildi: {cookie_file}")


async def load_cookies(company_name: str) -> bool:
    """
    Kaydedilmiş çerezleri yükler
    
    Args:
        company_name: Şirket adı (dosya adı için)
        
    Returns:
        bool: Çerezler başarıyla yüklendiyse True
    """
    global _context
    
    if _context is None:
        print("⚠ Context bulunamadı, çerezler yüklenemedi")
        return False
    
    cookies_dir = Path("storage/cookies")
    cookie_file = cookies_dir / f"{company_name}.json"
    
    if not cookie_file.exists():
        print(f"⚠ Çerez dosyası bulunamadı: {cookie_file}")
        return False
    
    try:
        with open(cookie_file, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        
        await _context.add_cookies(cookies)
        print(f"✓ Çerezler yüklendi: {cookie_file}")
        return True
    except Exception as e:
        print(f"✗ Çerez yükleme hatası: {e}")
        return False
