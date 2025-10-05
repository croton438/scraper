import os
import pyotp
from dotenv import load_dotenv
from pathlib import Path
from playwright.async_api import TimeoutError as PlaywrightTimeout
from utils.browser import new_page, close_page, save_cookies

load_dotenv()

SOMPO_USER = os.getenv("SOMPO_USER")
SOMPO_PASS = os.getenv("SOMPO_PASS")
SOMPO_TOTP_SECRET = os.getenv("SOMPO_TOTP_SECRET")
SOMPO_LOGIN_URL = os.getenv("SOMPO_LOGIN_URL", "https://ejento.somposigorta.com.tr/dashboard/login")

async def login():
    """
    Sompo portalına giriş yapar:
    1. Login URL'ye gider
    2. Kullanıcı adı ve şifre ile giriş yapar
    3. Google Authenticator (TOTP) kodu ile 2FA doğrulama yapar
    """
    page = await new_page()
    try:
        print("🔐 [1/4] Login URL'ye gidiliyor:", SOMPO_LOGIN_URL)
        await page.goto(SOMPO_LOGIN_URL, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_load_state("networkidle")

        print("👤 [2/4] Kullanıcı adı ve şifre giriliyor...")
        # Username
        await page.fill('input[name="username"]', SOMPO_USER)
        # Password
        await page.fill('input[name="password"]', SOMPO_PASS)
        # Giriş butonu
        await page.click('button[type="submit"]')

        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(1500)

        print("🔑 [3/4] Google Authenticator kodu ile doğrulama yapılıyor...")
        # TOTP (Google Authenticator)
        if SOMPO_TOTP_SECRET:
            try:
                await page.wait_for_selector('input[type="text"]', timeout=5000)
                code = pyotp.TOTP(SOMPO_TOTP_SECRET).now()
                print(f"   → TOTP Kodu: {code}")
                await page.fill('input[type="text"]', code)
                await page.press('input[type="text"]', "Enter")
            except PlaywrightTimeout:
                print("   ⚠ TOTP ekranı bulunamadı, devam ediliyor...")

        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(1500)

        print("💾 [4/4] Oturum bilgileri kaydediliyor...")
        # Cookies kaydet
        Path("storage/cookies").mkdir(parents=True, exist_ok=True)
        await save_cookies("sompo", page)

        # Screenshot
        Path("logs").mkdir(exist_ok=True)
        await page.screenshot(path="logs/sompo_after_login.png", full_page=True)

        print("✅ Sompo login başarılı!")
        return {
            "ok": True, 
            "msg": "Sompo login tamamlandı", 
            "url": page.url,
            "screenshot": "logs/sompo_after_login.png"
        }

    except Exception as e:
        print(f"❌ Login hatası: {str(e)}")
        Path("logs").mkdir(exist_ok=True)
        await page.screenshot(path="logs/sompo_LOGIN_ERROR.png", full_page=True)
        return {
            "ok": False, 
            "error": str(e),
            "screenshot": "logs/sompo_LOGIN_ERROR.png"
        }

    finally:
        await close_page(page)
