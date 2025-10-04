"""
FastAPI Ana Dosyası - Scraper API
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from portals import sompo

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Scraper API başlatıldı")
    print("📚 Dokümantasyon: http://localhost:8000/docs")
    print("⚠ .env dosyasında şu değişkenler olmalı:")
    print("   - SOMPO_USER")
    print("   - SOMPO_PASS")
    print("   - SOMPO_TOTP_SECRET (opsiyonel)")
    yield
    # Shutdown
    print("🛑 Scraper API kapatılıyor...")

app = FastAPI(
    title="Insurance Scraper API",
    description="Sigorta şirketleri için web scraping ve teklif alma API'si",
    version="1.0.0",
    lifespan=lifespan
)


class QuoteRequest(BaseModel):
    """Teklif alma için request modeli"""
    parameters: Dict[str, Any]


@app.get("/")
async def root():
    """API ana sayfası"""
    return {
        "message": "Insurance Scraper API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "sompo": {
                "login": "/sompo/login",
                "tamamlayici": "/sompo/tamamlayici"
            }
        }
    }


@app.get("/health")
async def health():
    """API sağlık kontrolü"""
    return {"status": "ok"}


@app.post("/sompo/login")
async def sompo_login():
    """
    Sompo portal'a login yapar
    
    .env dosyasında SOMPO_USER, SOMPO_PASS ve SOMPO_TOTP_SECRET olmalı
    """
    result = await sompo.login()
    if not result.get("ok"):
        raise HTTPException(status_code=401, detail=result.get("error", "Login başarısız"))
    return result


@app.post("/sompo/tamamlayici")
async def sompo_tamamlayici(request: QuoteRequest):
    """
    Sompo tamamlayıcı sağlık sigortası teklifi alır
    
    Önce /sompo/login ile giriş yapılmalı
    """
    result = await sompo.get_tamamlayici_quote(request.parameters)
    if not result.get("ok"):
        raise HTTPException(status_code=400, detail=result.get("error", "Teklif alınamadı"))
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
