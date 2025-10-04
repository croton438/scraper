import os
import pyotp
import json
from pathlib import Path
from dotenv import load_dotenv
from playwright.async_api import TimeoutError as PlaywrightTimeout
from utils.browser import new_page, close_page

load_dotenv()

SOMPO_USER = os.getenv("SOMPO_USER")
SOMPO_PASS = os.getenv("SOMPO_PASS")
SOMPO_TOTP_SECRET = os.getenv("SOMPO_TOTP_SECRET")
SOMPO_LOGIN_URL = os.getenv("SOMPO_LOGIN_URL", "https://ejento.somposigorta.com.tr/dashboard/login")


async def login():
    page = await new_page()
    try:
        await page.goto(SOMPO_LOGIN_URL, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_load_state("networkidle")

        # Username
        await page.fill('input[name="username"]', SOMPO_USER)

        # Password
        await page.fill('input[name="password"]', SOMPO_PASS)

        # Login butonu
        await page.click('button[type="submit"]')

        # TOTP (Google Auth)
        try:
            await page.wait_for_selector('input[type="text"][maxlength="6"]', timeout=5000)
            if SOMPO_TOTP_SECRET:
                totp = pyotp.TOTP(SOMPO_TOTP_SECRET).now()
                await page.fill('input[type="text"][maxlength="6"]', totp)
                await page.press('input[type="text"][maxlength="6"]', "Enter")
        except PlaywrightTimeout:
            print("TOTP alanı bulunamadı, belki bypass oldu")

        await page.wait_for_load_state("networkidle")

        # Çerez kaydet
        cookies = await page.context.cookies()
        cookies_dir = Path("storage/cookies")
        cookies_dir.mkdir(parents=True, exist_ok=True)
        with open(cookies_dir / "sompo.json", "w", encoding="utf-8") as f:
            json.dump(cookies, f, indent=2, ensure_ascii=False)

        return {"ok": True, "msg": "Sompo login başarılı", "cookies_saved": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        await close_page(page)


async def get_tamamlayici_quote(params: dict):
    page = await new_page()
    try:
        await page.goto(SOMPO_LOGIN_URL.replace("/login", ""), wait_until="networkidle")
        return {"ok": True, "msg": "Teklif sayfası açıldı (dummy)", "url": page.url}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        await close_page(page)
