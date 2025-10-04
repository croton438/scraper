import os
import pyotp
from dotenv import load_dotenv
from playwright.sync_api import TimeoutError as PlaywrightTimeout
from utils.browser import new_page, close_browser, save_cookies, load_cookies

load_dotenv()

SOMPO_USER = os.getenv("SOMPO_USER")
SOMPO_PASS = os.getenv("SOMPO_PASS")
SOMPO_TOTP_SECRET = os.getenv("SOMPO_TOTP_SECRET")
SOMPO_LOGIN_URL = os.getenv("SOMPO_LOGIN_URL", "https://ejento.somposigorta.com.tr/dashboard/login")


def login():
    """
    Sompo portal login
    """
    page = new_page()
    try:
        print(f"[*] Login URL'e gidiliyor: {SOMPO_LOGIN_URL}")
        page.goto(SOMPO_LOGIN_URL, timeout=30000)

        # Username
        page.fill('input[name="username"]', SOMPO_USER)
        page.fill('input[name="password"]', SOMPO_PASS)

        # Login button
        page.click('button[type="submit"]')

        # 2FA kontrol
        try:
            page.wait_for_selector('input[type="text"][maxlength="6"]', timeout=5000)
            if SOMPO_TOTP_SECRET:
                totp = pyotp.TOTP(SOMPO_TOTP_SECRET).now()
                page.fill('input[type="text"][maxlength="6"]', totp)
                page.click('button[type="submit"]')
        except PlaywrightTimeout:
            print("2FA ekranı çıkmadı, direkt dashboard olabilir.")

        page.wait_for_load_state("networkidle")

        # Çerezleri kaydet
        save_cookies("sompo")

        return {"ok": True, "msg": "Login başarılı", "url": page.url}

    except Exception as e:
        return {"ok": False, "error": str(e)}

    finally:
        close_browser()


def get_tamamlayici_quote(params: dict):
    """
    Tamamlayıcı sağlık sigortası teklifi alır
    """
    page = new_page()
    try:
        # Çerez yükle
        if not load_cookies("sompo"):
            result = login()
            if not result.get("ok"):
                return {"ok": False, "error": "Login başarısız"}
            load_cookies("sompo")

        # Dashboard
        dashboard_url = SOMPO_LOGIN_URL.replace("/login", "")
        page.goto(dashboard_url, timeout=30000)

        # Menüye tıkla
        try:
            page.click('text=Tamamlayıcı Sağlık', timeout=5000)
        except:
            return {"ok": False, "error": "Menü bulunamadı"}

        return {"ok": True, "msg": "Tamamlayıcı sağlık teklif sayfasına ulaşıldı", "url": page.url}

    except Exception as e:
        return {"ok": False, "error": str(e)}

    finally:
        close_browser()
