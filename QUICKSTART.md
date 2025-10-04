# 🚀 Hızlı Başlangıç Kılavuzu

## Windows PowerShell'de Kurulum

### 1️⃣ Projeyi İndirin/Klonlayın

```powershell
cd C:\Users\cifci\Desktop\scraper
```

### 2️⃣ Virtual Environment Oluşturun

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Not:** Eğer script çalıştırma hatası alırsanız:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3️⃣ Bağımlılıkları Yükleyin

```powershell
pip install -r requirements.txt
```

### 4️⃣ Playwright Browser'ı Yükleyin

```powershell
playwright install chromium
```

### 5️⃣ .env Dosyası Oluşturun

Kök dizinde `.env` dosyası oluşturun:

```env
SOMPO_USER=kullanici_adiniz
SOMPO_PASS=sifreniz
SOMPO_TOTP_SECRET=JBSWY3DPEHPK3PXP
SOMPO_LOGIN_URL=https://portal.sompo.com.tr/login
```

### 6️⃣ API'yi Çalıştırın

```powershell
python main.py
```

veya

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 7️⃣ Test Edin

Tarayıcınızda açın:
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## 📡 API Kullanımı

### PowerShell ile Test

```powershell
# Health Check
Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET

# Sompo Login
Invoke-WebRequest -Uri "http://localhost:8000/sompo/login" -Method POST

# Tamamlayıcı Teklif
$body = @{
    parameters = @{
        customer_name = "Ahmet Yılmaz"
        tc_no = "12345678901"
    }
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/sompo/tamamlayici" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

### curl ile Test (Git Bash varsa)

```bash
# Health Check
curl http://localhost:8000/health

# Sompo Login
curl -X POST http://localhost:8000/sompo/login

# Tamamlayıcı Teklif
curl -X POST http://localhost:8000/sompo/tamamlayici \
  -H "Content-Type: application/json" \
  -d '{"parameters": {"customer_name": "Ahmet Yılmaz"}}'
```

## 🔍 Klasör Yapısı

```
scraper/
│
├── main.py                 # ✅ FastAPI giriş noktası
├── requirements.txt        # ✅ Bağımlılıklar
├── .env                    # ⚠️ SİZ OLUŞTURUN (credentials)
├── README.md              # ✅ Ana dokümantasyon
├── QUICKSTART.md          # ✅ Bu dosya
│
├── utils/
│   ├── __init__.py        # ✅
│   └── browser.py         # ✅ Playwright yönetimi
│
├── portals/
│   ├── __init__.py        # ✅
│   ├── sompo.py          # ✅ Sompo entegrasyonu
│   ├── anadolu.py        # 🔜 Hazır şablon
│   ├── atlas.py          # 🔜 Hazır şablon
│   ├── koru.py           # 🔜 Hazır şablon
│   ├── quick.py          # 🔜 Hazır şablon
│   ├── doga.py           # 🔜 Hazır şablon
│   └── seker.py          # 🔜 Hazır şablon
│
├── storage/
│   └── cookies/           # Otomatik oluşur
│
├── logs/                  # Otomatik oluşur
│   ├── sompo_after_login.png
│   └── sompo_error.png
│
└── venv/                  # Virtual environment
```

## 🐛 Sorun Giderme

### 1. PowerShell Script Çalıştırma Hatası

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. Playwright Browser Kurulamıyor

```powershell
# Chromium'u manuel kur
playwright install chromium --force
```

### 3. Import Hataları

```powershell
# Virtual environment'ı aktif et
.\venv\Scripts\Activate.ps1

# Bağımlılıkları tekrar yükle
pip install -r requirements.txt --force-reinstall
```

### 4. Port 8000 Kullanımda

```powershell
# Farklı port kullan
python main.py --port 8001

# veya
uvicorn main:app --port 8001
```

### 5. Browser Headless Modda Çalışmıyor

`.env` dosyasında:
```env
HEADLESS=false
```

## 📞 Yardım

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

## ✅ Kontrol Listesi

- [ ] Python 3.8+ kurulu
- [ ] Virtual environment oluşturuldu
- [ ] `pip install -r requirements.txt` çalıştırıldı
- [ ] `playwright install chromium` çalıştırıldı
- [ ] `.env` dosyası oluşturuldu ve credentials eklendi
- [ ] `python main.py` ile API başlatıldı
- [ ] http://localhost:8000/docs açıldı
- [ ] `/sompo/login` endpoint'i test edildi

Başarılar! 🎉

