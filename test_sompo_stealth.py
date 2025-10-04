"""
Sompo Login - Stealth Mode (Bot Bypass)
"""
import asyncio
import os
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()

async def test_sompo_stealth():
    print("=" * 60)
    print("SOMPO LOGIN - STEALTH MODE")
    print("=" * 60)
    
    playwright = await async_playwright().start()
    
    # Stealth ayarları ile browser başlat
    browser = await playwright.chromium.launch(
        headless=False,
        slow_mo=500,
        args=[
            '--disable-blink-features=AutomationControlled',
            '--disable-dev-shm-usage',
            '--disable-web-security',
            '--no-sandbox',
        ]
    )
    
    # Gerçek browser gibi context oluştur
    context = await browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        locale='tr-TR',
        timezone_id='Europe/Istanbul',
    )
    
    # Automation detection'ı kaldır
    await context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """)
    
    page = await context.new_page()
    
    try:
        # URL'leri deneyelim
        urls_to_try = [
            "https://ejento.somposigorta.com.tr",
            "https://ejento.somposigorta.com.tr/login",
            "https://ejento.somposigorta.com.tr/dashboard/login",
        ]
        
        for i, url in enumerate(urls_to_try, 1):
            print(f"\n[{i}] Deneniyor: {url}")
            try:
                response = await page.goto(url, wait_until="load", timeout=20000)
                if response:
                    print(f"[OK] Yuklendi! Status: {response.status}")
                    print(f"[OK] Final URL: {page.url}")
                    await page.screenshot(path=f"logs/stealth_success_{i}.png")
                    
                    # Form elemanlarını kontrol et
                    print("\n[*] Input alanları aranıyor...")
                    inputs = await page.query_selector_all('input')
                    print(f"[*] {len(inputs)} input bulundu")
                    
                    if len(inputs) > 0:
                        print("[OK] Login formu bu sayfada!")
                        
                        # 10 saniye bekle
                        print("\n[!] 10 saniye bekleniyor - sayfayı inceleyin...")
                        await asyncio.sleep(10)
                        
                        # Username ve password doldur
                        print("\n[*] Login bilgileri dolduruluyor...")
                        
                        # İlk text input
                        text_input = await page.query_selector('input[type="text"], input[type="email"], input:not([type="password"]):not([type="hidden"])')
                        if text_input:
                            username = os.getenv("SOMPO_USER", "BULUT1")
                            await text_input.fill(username)
                            print(f"[OK] Username girildi: {username}")
                            await asyncio.sleep(1)
                        
                        # Password input
                        pass_input = await page.query_selector('input[type="password"]')
                        if pass_input:
                            password = os.getenv("SOMPO_PASS", "EEsigorta..28")
                            await pass_input.fill(password)
                            print("[OK] Password girildi")
                            await asyncio.sleep(1)
                        
                        await page.screenshot(path="logs/stealth_form_filled.png")
                        
                        print("\n[!] 20 saniye bekleniyor - manuel devam edebilirsiniz...")
                        await asyncio.sleep(20)
                        
                        break
                    else:
                        print("[!] Bu sayfada form yok, diğer URL deneniyor...")
                        
            except Exception as e:
                print(f"[ERROR] {url} hatasi: {str(e)}")
                continue
        
        await page.screenshot(path="logs/stealth_final.png")
        
    except Exception as e:
        print(f"\n[ERROR] Genel hata: {str(e)}")
        try:
            await page.screenshot(path="logs/stealth_error.png")
        except:
            pass
    finally:
        print("\n[*] Browser kapatiliyor (5 saniye sonra)...")
        await asyncio.sleep(5)
        await browser.close()
        await playwright.stop()
    
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_sompo_stealth())

