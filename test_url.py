"""
URL Erişim Test - Basit browser testi
"""
import asyncio
from playwright.async_api import async_playwright

async def test_url():
    print("=" * 60)
    print("URL ERISIM TESTI")
    print("=" * 60)
    
    url = "https://ejento.somposigorta.com.tr/dashboard/login"
    print(f"\n[*] Test URL: {url}")
    
    async with async_playwright() as p:
        print("[*] Browser baslatiliyor...")
        browser = await p.chromium.launch(headless=False)
        
        print("[*] Yeni sayfa aciliyor...")
        page = await browser.new_page()
        
        try:
            print(f"[*] URL'e gidiliyor: {url}")
            print("[!] DIKKAT: 10 saniye timeout var...")
            
            response = await page.goto(url, wait_until="domcontentloaded", timeout=10000)
            
            if response:
                print(f"[OK] Sayfa yuklendi!")
                print(f"[OK] Status: {response.status}")
                print(f"[OK] URL: {page.url}")
                
                # Screenshot al
                await page.screenshot(path="logs/url_test_SUCCESS.png")
                print("[OK] Screenshot kaydedildi: logs/url_test_SUCCESS.png")
                
                # 5 saniye bekle (inceleme için)
                print("[*] 5 saniye bekleniyor...")
                await asyncio.sleep(5)
            else:
                print("[ERROR] Response alinamadi")
                
        except Exception as e:
            print(f"[ERROR] Hata: {str(e)}")
            
            # Hata screenshot'i
            try:
                await page.screenshot(path="logs/url_test_ERROR.png")
                print("[*] Hata screenshot: logs/url_test_ERROR.png")
            except:
                pass
                
        finally:
            print("[*] Browser kapatiliyor...")
            await browser.close()
    
    print("=" * 60)
    print("TEST TAMAMLANDI")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_url())

