"""
FastAPI Ana Dosyası - Scraper API
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from portals import sompo


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Scraper API başlatıldı")
    yield
    print("🛑 Scraper API kapatılıyor...")


app = FastAPI(
    title="Insurance Scraper API",
    description="Sigorta şirketleri için web scraping API",
    version="1.0.0",
    lifespan=lifespan
)


class QuoteRequest(BaseModel):
    parameters: Dict[str, Any]


@app.get("/")
async def root():
    return {"status": "running", "docs": "/docs"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/sompo/login")
async def sompo_login():
    result = await sompo.login()
    if not result.get("ok"):
        raise HTTPException(status_code=401, detail=result.get("error", "Login başarısız"))
    return result


@app.post("/sompo/tamamlayici")
async def sompo_tamamlayici(request: QuoteRequest):
    result = await sompo.get_tamamlayici_quote(request.parameters)
    if not result.get("ok"):
        raise HTTPException(status_code=400, detail=result.get("error", "Teklif alınamadı"))
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
