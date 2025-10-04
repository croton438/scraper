# portals/sompo.py
import os
import time
import pyotp
from dotenv import load_dotenv
from playwright.async_api import Page, TimeoutError as PlaywrightTimeout
from utils.browser import new_page, close_page, save_cookies, load_cookies

load_dotenv()

SOMPO_USER = os.getenv("SOMPO_USER")
SOMPO_PASS = os.getenv("SOMPO_PASS")
SOMPO_TOTP_SECRET = os.getenv("SOMPO_TOTP_SECRET")
SOMPO_LOGIN_URL = os.getenv("SOMPO_LOGIN_URL", "https://ejento.somposigorta.com.tr/dashboard/login")

async def login():
    """
    Sompo Sigorta portal'a login yapar
    URL: https://ejento.somposigorta.com.tr/dashboard/login
    """
    # Her login için yeni browser instance oluştur
    from playwright.async_api import async_playwright
    
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    page = await browser.new_page()
    
    try:
        print(f"[*] Login URL'e gidiliyor: {SOMPO_LOGIN_URL}")
        await page.goto(SOMPO_LOGIN_URL, wait_until="domcontentloaded", timeout=30000)
        
        # Sayfa yüklenene kadar bekle
        await page.wait_for_load_state("networkidle")
        
        # İlk screenshot - login sayfası
        os.makedirs("logs", exist_ok=True)
        await page.screenshot(path="logs/sompo_01_login_page.png")
        
        # Username input'u bekle ve doldur
        print(f"[+] Username giriliyor: {SOMPO_USER}")
        username_selectors = [
            'input[name="username"]',
            'input[id="username"]',
            'input[type="text"]',
            '#username',
            'input[placeholder*="Kullanıcı"]',
            'input[placeholder*="kullanıcı"]',
        ]
        
        username_filled = False
        for selector in username_selectors:
            try:
                await page.wait_for_selector(selector, timeout=2000)
                await page.fill(selector, SOMPO_USER)
                username_filled = True
                print(f"[OK] Username selector bulundu: {selector}")
                break
            except:
                continue
        
        if not username_filled:
            raise Exception("Username input bulunamadı")
        
        # Password input'u bekle ve doldur
        print("[+] Password giriliyor...")
        password_selectors = [
            'input[name="password"]',
            'input[id="password"]',
            'input[type="password"]',
            '#password',
        ]
        
        password_filled = False
        for selector in password_selectors:
            try:
                await page.wait_for_selector(selector, timeout=2000)
                await page.fill(selector, SOMPO_PASS)
                password_filled = True
                print(f"[OK] Password selector bulundu: {selector}")
                break
            except:
                continue
        
        if not password_filled:
            raise Exception("Password input bulunamadı")
        
        # Screenshot - credentials girildi
        await page.screenshot(path="logs/sompo_02_credentials_filled.png")
        
        # Login butonuna tıkla
        print("[+] Login butonuna tıklanıyor...")
        login_button_selectors = [
            'button[type="submit"]',
            'button:has-text("Giriş")',
            'button:has-text("GİRİŞ")',
            'input[type="submit"]',
            '.login-button',
            '#login-button',
        ]
        
        button_clicked = False
        for selector in login_button_selectors:
            try:
                await page.click(selector, timeout=2000)
                button_clicked = True
                print(f"[OK] Login button selector bulundu: {selector}")
                break
            except:
                continue
        
        if not button_clicked:
            raise Exception("Login button bulunamadı")
        
        # Sayfanın yüklenmesini bekle
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(2000)
        
        # TOTP (2FA) kontrolü
        print("[+] 2FA kontrolü yapılıyor...")
        totp_selectors = [
            'input[name="otp"]',
            'input[name="code"]',
            'input[name="token"]',
            'input[placeholder*="kod"]',
            'input[placeholder*="Kod"]',
            'input[type="text"][maxlength="6"]',
        ]
        
        totp_found = False
        for selector in totp_selectors:
            try:
                await page.wait_for_selector(selector, timeout=3000)
                print(f"[OK] TOTP input bulundu: {selector}")
                
                # TOTP kodu oluştur ve gir
                if SOMPO_TOTP_SECRET:
                    totp = pyotp.TOTP(SOMPO_TOTP_SECRET).now()
                    print(f"[CODE] TOTP kodu: {totp}")
                    await page.fill(selector, totp)
                    
                    # Screenshot - TOTP girildi
                    await page.screenshot(path="logs/sompo_03_totp_filled.png")
                    
                    # TOTP submit butonu
                    await page.wait_for_timeout(500)
                    try:
                        await page.click('button[type="submit"]', timeout=2000)
                    except:
                        await page.press(selector, 'Enter')
                    
                    totp_found = True
                    break
                else:
                    raise Exception("TOTP secret .env dosyasında tanımlı değil")
                    
            except PlaywrightTimeout:
                continue
        
        if not totp_found:
            print("[!] TOTP input bulunamadı, direkt dashboard'a yönlendirilmiş olabilir")
        
        # Login başarı kontrolü - dashboard bekle
        print("[+] Dashboard yüklenmesi bekleniyor...")
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(3000)
        
        # Dashboard kontrolü (çeşitli selector'lar dene)
        dashboard_selectors = [
            'text=Dashboard',
            'text=Anasayfa',
            'text=Hoş Geldiniz',
            '.dashboard',
            '#dashboard',
            'nav',
            '.sidebar',
            '.user-menu',
        ]
        
        dashboard_found = False
        for selector in dashboard_selectors:
            try:
                await page.wait_for_selector(selector, timeout=3000)
                dashboard_found = True
                print(f"[OK] Dashboard elementi bulundu: {selector}")
                break
            except:
                continue
        
        # Final screenshot
        await page.screenshot(path="logs/sompo_04_after_login.png", full_page=True)
        current_url = page.url
        print(f"[URL] Mevcut URL: {current_url}")
        
        # Çerezleri kaydet
        import json
        from pathlib import Path
        cookies_dir = Path("storage/cookies")
        cookies_dir.mkdir(parents=True, exist_ok=True)
        cookies = await page.context.cookies()
        cookie_file = cookies_dir / "sompo.json"
        with open(cookie_file, 'w', encoding='utf-8') as f:
            json.dump(cookies, f, indent=2, ensure_ascii=False)
        print("[COOKIE] Çerezler kaydedildi: storage/cookies/sompo.json")
        
        if dashboard_found or "dashboard" in current_url.lower():
            return {
                "ok": True, 
                "msg": "Sompo login başarılı",
                "url": current_url,
                "cookies_saved": True
            }
        else:
            return {
                "ok": False,
                "msg": "Login başarılı görünüyor ama dashboard bulunamadı",
                "url": current_url,
                "warning": "Manuel kontrol gerekebilir"
            }
            
    except Exception as e:
        # Hata durumunda screenshot al
        os.makedirs("logs", exist_ok=True)
        try:
            await page.screenshot(path="logs/sompo_ERROR.png", full_page=True)
        except:
            pass
        print(f"[ERROR] Login hatasi: {str(e)}")
        
        return {"ok": False, "error": str(e)}
    finally:
        try:
            await page.close()
            await browser.close()
            await playwright.stop()
        except:
            pass


async def get_tamamlayici_quote(params: dict):
    """
    Tamamlayıcı sağlık sigortası teklifi alır
    
    Args:
        params: Teklif parametreleri (tc_no, dogum_tarihi, vs.)
        
    Returns:
        dict: Teklif sonuçları
    """
    page = await new_page()
    try:
        print("[*] Teklif alma işlemi başlıyor...")
        
        # Önce çerezleri yükle (login durumu için)
        cookies_loaded = await load_cookies("sompo")
        
        if not cookies_loaded:
            # Çerezler yoksa önce login yap
            print("[!] Çerez bulunamadı, login yapılıyor...")
            login_result = await login()
            if not login_result.get("ok"):
                return {"ok": False, "error": "Login başarısız. Önce /sompo/login çağırın"}
            
            # Login sonrası çerezleri tekrar yükle
            await load_cookies("sompo")
        
        # Dashboard'a git
        dashboard_url = SOMPO_LOGIN_URL.replace("/login", "")
        print(f"[*] Dashboard'a gidiliyor: {dashboard_url}")
        await page.goto(dashboard_url, wait_until="networkidle", timeout=30000)
        
        # Screenshot - dashboard
        os.makedirs("logs", exist_ok=True)
        await page.screenshot(path="logs/sompo_teklif_01_dashboard.png", full_page=True)
        
        # Tamamlayıcı sağlık menüsünü bul
        print("[*] Tamamlayıcı sağlık menüsü aranıyor...")
        tamamlayici_selectors = [
            'text=Tamamlayıcı',
            'text=Tamamlayıcı Sağlık',
            'a:has-text("Tamamlayıcı")',
            'a:has-text("Sağlık")',
            '[href*="tamamlayici"]',
            '[href*="saglik"]',
        ]
        
        menu_found = False
        for selector in tamamlayici_selectors:
            try:
                await page.click(selector, timeout=3000)
                menu_found = True
                print(f"[OK] Tamamlayıcı menü bulundu: {selector}")
                await page.wait_for_load_state("networkidle")
                await page.wait_for_timeout(2000)
                break
            except:
                continue
        
        if not menu_found:
            # Menü bulunamazsa, doğrudan URL'i dene
            possible_urls = [
                f"{dashboard_url}/tamamlayici-saglik",
                f"{dashboard_url}/teklif/tamamlayici",
                f"{dashboard_url}/saglik-sigortasi",
            ]
            
            for url in possible_urls:
                try:
                    print(f"[*] Direkt URL deneniyor: {url}")
                    await page.goto(url, wait_until="networkidle", timeout=10000)
                    menu_found = True
                    break
                except:
                    continue
        
        if not menu_found:
            await page.screenshot(path="logs/sompo_teklif_ERROR_menu_not_found.png", full_page=True)
            return {
                "ok": False, 
                "error": "Tamamlayıcı sağlık menüsü bulunamadı",
                "info": "Portal menü yapısı incelenmelidir"
            }
        
        # Teklif sayfası screenshot
        await page.screenshot(path="logs/sompo_teklif_02_form_page.png", full_page=True)
        print(f"[URL] Teklif sayfası URL: {page.url}")
        
        # Form alanlarını bul ve doldur
        # TODO: Gerçek form selector'ları portal'a göre eklenmeli
        print("[*] Form alanları doldurulacak...")
        
        # Örnek: TC Kimlik No
        if params.get("tc_no"):
            tc_selectors = ['input[name="tc"]', 'input[id="tcKimlikNo"]', 'input[placeholder*="TC"]']
            for selector in tc_selectors:
                try:
                    await page.fill(selector, params["tc_no"], timeout=2000)
                    print(f"[OK] TC No girildi: {selector}")
                    break
                except:
                    continue
        
        # Örnek: Doğum Tarihi
        if params.get("dogum_tarihi"):
            dob_selectors = ['input[name="dogumTarihi"]', 'input[type="date"]']
            for selector in dob_selectors:
                try:
                    await page.fill(selector, params["dogum_tarihi"], timeout=2000)
                    print(f"[OK] Doğum tarihi girildi: {selector}")
                    break
                except:
                    continue
        
        # Form screenshot
        await page.screenshot(path="logs/sompo_teklif_03_form_filled.png", full_page=True)
        
        return {
            "ok": True,
            "msg": "Teklif sayfasına ulaşıldı - Form implementasyonu devam ediyor",
            "url": page.url,
            "info": "Portal'daki form alanları logs/ klasöründeki screenshot'larda incelenebilir",
            "next_steps": [
                "Form selector'larını belirle",
                "Teklif hesaplama butonunu bul",
                "Sonuç sayfasını parse et"
            ]
        }
        
    except Exception as e:
        os.makedirs("logs", exist_ok=True)
        await page.screenshot(path="logs/sompo_teklif_ERROR.png", full_page=True)
        print(f"[ERROR] Teklif alma hatasi: {str(e)}")
        return {"ok": False, "error": str(e), "url": page.url}
    finally:
        await close_page(page)
