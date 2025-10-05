import uvicorn
from fastapi import FastAPI
from portals import sompo

app = FastAPI(title="Sompo Login Otomasyonu")

@app.on_event("startup")
async def startup_event():
    print("🚀 Sompo Login API başlatıldı")
    print("📝 Kullanım: POST /sompo/login")

@app.on_event("shutdown")
async def shutdown_event():
    print("🛑 API kapatılıyor...")

@app.post("/sompo/login")
async def sompo_login():
    """
    Sompo portalına giriş yapar:
    - Kullanıcı adı ve şifre ile giriş
    - Google Authenticator (TOTP) ile 2FA doğrulama
    """
    try:
        result = await sompo.login()
        return result
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, loop="asyncio")
