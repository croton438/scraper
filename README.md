# Insurance Scraper API 🚀

FastAPI + Playwright kullanarak sigorta şirketleri portal entegrasyonları.

## 📁 Proje Yapısı

```
scraper/
│── main.py                 # FastAPI giriş noktası
│── requirements.txt        # Python bağımlılıkları
│── README.md              # Bu dosya
│
├── utils/
│   ├── __init__.py
│   └── browser.py         # Playwright browser yönetimi
│
├── portals/
│   ├── __init__.py
│   ├── sompo.py          # Sompo Sigorta (✅ İmplemente)
│   ├── anadolu.py        # Anadolu Sigorta (🔜 Yakında)
│   ├── atlas.py          # Atlas Sigorta (🔜 Yakında)
│   ├── koru.py           # Koru Sigorta (🔜 Yakında)
│   ├── quick.py          # Quick Sigorta (🔜 Yakında)
│   ├── doga.py           # Doğa Sigorta (🔜 Yakında)
│   └── seker.py          # Şeker Sigorta (🔜 Yakında)
│
└── storage/
    └── cookies/           # Portal çerezleri (otomatik kaydedilir)
```

## 🔧 Kurulum

### 1. Sanal ortam oluştur (önerilen)

```powershell
# Windows PowerShell
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 2. Bağımlılıkları yükle

```powershell
pip install -r requirements.txt
```

### 3. Playwright browser'larını yükle

```powershell
playwright install chromium
```

### 4. .env dosyası oluştur

Kök dizinde `.env` dosyası oluşturun:

```env
# Sompo Sigorta Credentials
SOMPO_USER=kullanici_adiniz
SOMPO_PASS=sifreniz
SOMPO_TOTP_SECRET=base32_secret_key  # Opsiyonel, 2FA varsa
SOMPO_LOGIN_URL=https://portal.sompo.com.tr/login

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
HEADLESS=true
```

**TOTP Secret Nasıl Alınır?**
- 2FA kurulumunda gösterilen QR kodunu kopyalayın
- Base32 formatındaki secret key'i alın
- `.env` dosyasına ekleyin

## 🚀 Çalıştırma

### Development Modu (Auto-reload)

```bash
python main.py
```

veya

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Modu

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

API şu adreste çalışacaktır: `http://localhost:8000`

Swagger UI: `http://localhost:8000/docs`

## 📡 API Kullanımı

### Sompo Sigorta

#### 1. Login (Otomatik - .env'den okur)

```bash
POST http://localhost:8000/sompo/login
```

**Not:** `.env` dosyasında `SOMPO_USER`, `SOMPO_PASS` ve `SOMPO_TOTP_SECRET` olmalı.

#### 2. Tamamlayıcı Sağlık Teklifi

```bash
POST http://localhost:8000/sompo/tamamlayici
Content-Type: application/json

{
  "parameters": {
    "customer_name": "Ahmet Yılmaz",
    "tc_no": "12345678901",
    "package": "premium"
  }
}
```

#### PowerShell'de Test

```powershell
# Login
Invoke-RestMethod -Uri "http://localhost:8000/sompo/login" -Method POST

# Teklif
$body = @{
    parameters = @{
        customer_name = "Ahmet Yılmaz"
        tc_no = "12345678901"
    }
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/sompo/tamamlayici" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

### Health Check

```bash
GET http://localhost:8000/health
```

## 🔐 Çerez Yönetimi

- Login sonrası çerezler otomatik olarak `storage/cookies/{company}.json` dosyasına kaydedilir
- Sonraki isteklerde çerezler otomatik yüklenir, yeniden login gerekmez
- Çerezler geçersiz olduğunda otomatik olarak yeniden login yapılır

## 🎯 Yeni Şirket Ekleme

1. `portals/` klasörüne yeni dosya oluştur (örn: `yeni_sirket.py`)
2. `BrowserManager` kullanarak login ve teklif fonksiyonları yaz
3. `main.py` dosyasına endpoint'leri ekle

Örnek şablon:

```python
from utils.browser import BrowserManager

class YeniSirketPortal:
    def __init__(self):
        self.browser_manager = BrowserManager()
        self.company_name = "yeni_sirket"
        self.base_url = "https://portal-url.com"
    
    async def login(self, email: str, password: str):
        # Login implementasyonu
        pass
    
    async def get_quote(self, parameters: dict):
        # Teklif alma implementasyonu
        pass
    
    async def close(self):
        await self.browser_manager.close_browser()
```

## 📝 Özellikler

- ✅ Otomatik çerez yönetimi (login persistence)
- ✅ Google Auth desteği
- ✅ Screenshot alma (hata durumlarında)
- ✅ Headless/Headful mod desteği
- ✅ FastAPI ile RESTful API
- ✅ Swagger UI dokümantasyonu
- ✅ Modüler ve genişletilebilir yapı

## 🛠️ Teknolojiler

- **FastAPI**: Modern, hızlı web framework
- **Playwright**: Browser automation
- **Uvicorn**: ASGI server
- **Pydantic**: Veri validasyonu

## 📌 Notlar

- İlk login sırasında browser açılacaktır (headless=False)
- Google Auth için manuel 2FA girişi gerekebilir
- Portal selector'ları gerçek URL'lere göre güncellenmeli
- Production'da headless=True kullanılabilir

## 🚧 Geliştirme Durumu

| Şirket | Login | Teklif | Durum |
|--------|-------|--------|-------|
| Sompo | ✅ | 🔄 | Beta |
| Anadolu | 🔜 | 🔜 | Planlı |
| Atlas | 🔜 | 🔜 | Planlı |
| Koru | 🔜 | 🔜 | Planlı |
| Quick | 🔜 | 🔜 | Planlı |
| Doğa | 🔜 | 🔜 | Planlı |
| Şeker | 🔜 | 🔜 | Planlı |

## 📞 İletişim

Sorularınız için issue açabilirsiniz.

