"""
Sompo Login - Adım Adım Test
"""
import asyncio
import os
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()

async def test_sompo():
    print("=" * 60)
    print("SOMPO LOGIN - ADIM ADIM TEST")
    print("=" * 60)
    
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False, slow_mo=1000)
    page = await browser.new_page()
    
    try:
        # 1. Ana sayfaya git
        print("\n[1] Ana sayfaya gidiliyor...")
        base_url = "https://ejento.somposigorta.com.tr"
        await page.goto(base_url, timeout=30000)
        print(f"[OK] Ana sayfa yuklendi: {page.url}")
        await page.screenshot(path="logs/step1_homepage.png")
        await asyncio.sleep(2)
        
        # 2. Login sayfasına git
        print("\n[2] Login sayfasina gidiliyor...")
        login_url = f"{base_url}/dashboard/login"
        await page.goto(login_url, timeout=30000)
        print(f"[OK] Login sayfasi yuklendi: {page.url}")
        await page.screenshot(path="logs/step2_login_page.png")
        await asyncio.sleep(2)
        
        # 3. Username/Password alanlarını bul
        print("\n[3] Login formunu ariyorum...")
        
        # Sayfadaki tüm input'ları listele
        inputs = await page.query_selector_all('input')
        print(f"[*] Toplam {len(inputs)} input alani bulundu")
        
        for i, inp in enumerate(inputs):
            inp_type = await inp.get_attribute('type')
            inp_name = await inp.get_attribute('name')
            inp_id = await inp.get_attribute('id')
            inp_placeholder = await inp.get_attribute('placeholder')
            print(f"  Input {i+1}: type={inp_type}, name={inp_name}, id={inp_id}, placeholder={inp_placeholder}")
        
        # 4. Username gir
        print("\n[4] Username giriliyor...")
        username = os.getenv("SOMPO_USER", "BULUT1")
        
        # Farklı selector'ları dene
        selectors = [
            'input[type="text"]',
            'input[type="email"]',
            'input[name="username"]',
            'input[name="email"]',
            'input[id="username"]',
        ]
        
        username_filled = False
        for selector in selectors:
            try:
                elem = await page.query_selector(selector)
                if elem:
                    await elem.fill(username)
                    username_filled = True
                    print(f"[OK] Username girildi (selector: {selector})")
                    break
            except:
                continue
        
        if not username_filled:
            print("[ERROR] Username input bulunamadi!")
            # Manuel olarak doldur
            await asyncio.sleep(30)  # 30 saniye bekle
            return
        
        await page.screenshot(path="logs/step3_username_filled.png")
        await asyncio.sleep(1)
        
        # 5. Password gir
        print("\n[5] Password giriliyor...")
        password = os.getenv("SOMPO_PASS", "EEsigorta..28")
        
        password_input = await page.query_selector('input[type="password"]')
        if password_input:
            await password_input.fill(password)
            print("[OK] Password girildi")
        else:
            print("[ERROR] Password input bulunamadi!")
        
        await page.screenshot(path="logs/step4_password_filled.png")
        await asyncio.sleep(1)
        
        # 6. Login butonuna tıkla
        print("\n[6] Login butonuna tiklanacak...")
        print("[!] 5 saniye sonra login butonuna tiklanacak...")
        await asyncio.sleep(5)
        
        button_selectors = [
            'button[type="submit"]',
            'input[type="submit"]',
            'button:has-text("Giriş")',
            'button:has-text("GİRİŞ")',
        ]
        
        for selector in button_selectors:
            try:
                btn = await page.query_selector(selector)
                if btn:
                    await btn.click()
                    print(f"[OK] Login button tiklandi (selector: {selector})")
                    break
            except:
                continue
        
        # 7. Sayfanın yüklenmesini bekle
        print("\n[7] Sayfa yuklenmesi bekleniyor...")
        await asyncio.sleep(5)
        await page.screenshot(path="logs/step5_after_click.png")
        
        print(f"\n[URL] Mevcut URL: {page.url}")
        print("\n[*] 10 saniye daha bekleniyor (inceleme icin)...")
        await asyncio.sleep(10)
        
        await page.screenshot(path="logs/step6_final.png")
        
    except Exception as e:
        print(f"\n[ERROR] Hata: {str(e)}")
        await page.screenshot(path="logs/error_step_by_step.png")
    finally:
        print("\n[*] Browser kapatiliyor...")
        await browser.close()
        await playwright.stop()
    
    print("=" * 60)
    print("TEST TAMAMLANDI")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_sompo())

