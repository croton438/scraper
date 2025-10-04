"""
Google test - Playwright çalışıyor mu?
"""
import asyncio
from playwright.async_api import async_playwright

async def test_google():
    print("=" * 60)
    print("PLAYWRIGHT TEST - GOOGLE")
    print("=" * 60)
    
    async with async_playwright() as p:
        print("[*] Browser baslatiliyor...")
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        try:
            print("[*] Google'a gidiliyor...")
            await page.goto("https://www.google.com", timeout=10000)
            print(f"[OK] Basarili! URL: {page.url}")
            
            await asyncio.sleep(3)
            
            print("\n[*] Simdi Sompo URL'ini deniyoruz...")
            sompo_url = "https://ejento.somposigorta.com.tr"
            print(f"[*] URL: {sompo_url}")
            
            await page.goto(sompo_url, timeout=15000)
            print(f"[OK] Sompo ana sayfa yuklendi!")
            print(f"[OK] URL: {page.url}")
            
            await page.screenshot(path="logs/sompo_homepage.png")
            print("[OK] Screenshot: logs/sompo_homepage.png")
            
            await asyncio.sleep(5)
            
        except Exception as e:
            print(f"[ERROR] {str(e)}")
            await page.screenshot(path="logs/error_google_test.png")
        finally:
            await browser.close()
    
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_google())

