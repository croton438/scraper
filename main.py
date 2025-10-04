from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from portals import sompo

app = FastAPI(
    title="Insurance Scraper API",
    description="Sigorta scraping API",
    version="1.0.0"
)


class QuoteRequest(BaseModel):
    parameters: Dict[str, Any]


@app.get("/")
def root():
    return {"status": "running", "endpoints": ["/sompo/login", "/sompo/tamamlayici"]}


@app.post("/sompo/login")
def sompo_login():
    result = sompo.login()
    if not result.get("ok"):
        raise HTTPException(status_code=401, detail=result.get("error"))
    return result


@app.post("/sompo/tamamlayici")
def sompo_tamamlayici(request: QuoteRequest):
    result = sompo.get_tamamlayici_quote(request.parameters)
    if not result.get("ok"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result
