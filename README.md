# 🔐 Sompo Login Otomasyonu

Playwright kullanarak Sompo Sigorta portalına otomatik giriş yapan basit bir API.

## ✨ Özellikler

- ✅ Kullanıcı adı ve şifre ile otomatik giriş
- ✅ Google Authenticator (TOTP) ile 2FA doğrulama
- ✅ Oturum bilgilerini otomatik kaydetme (cookies)
- ✅ Hata durumunda ekran görüntüsü alma
- ✅ FastAPI ile REST API

## 📁 Proje Yapısı

```
scraper/
│── main.py                 # FastAPI giriş noktası
│── requirements.txt        # Python bağımlılıkları
│── CONFIG.md              # Konfigürasyon ayarları
│
├── utils/
│   └── browser.py         # Playwright browser yönetimi
│
├── portals/
│   └── sompo.py          # Sompo login modülü
│
├── storage/
│   └── cookies/           # Oturum bilgileri (otomatik oluşur)
│
└── logs/                  # Ekran görüntüleri (otomatik oluşur)
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
# Sompo Login Bilgileri
SOMPO_LOGIN_URL=https://ejento.somposigorta.com.tr/dashboard/login
SOMPO_USER=kullanici_adiniz
SOMPO_PASS=sifreniz
SOMPO_TOTP_SECRET=your_totp_secret_key_here
```

> 📖 Detaylı konfigürasyon bilgisi için [CONFIG.md](CONFIG.md) dosyasına bakın.

## 🚀 Çalıştırma

```powershell
python main.py
```

API şu adreste çalışacaktır: `http://localhost:8000`

Swagger UI (API Dokümantasyonu): `http://localhost:8000/docs`

## 📡 API Kullanımı

### Sompo Login

```bash
POST http://localhost:8000/sompo/login
```

**Not:** `.env` dosyasında `SOMPO_USER`, `SOMPO_PASS` ve `SOMPO_TOTP_SECRET` değerleri olmalı.

#### PowerShell'de Test

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/sompo/login" -Method POST
```

#### Curl ile Test

```bash
curl -X POST http://localhost:8000/sompo/login
```

#### Başarılı Yanıt Örneği

```json
{
  "ok": true,
  "msg": "Sompo login tamamlandı",
  "url": "https://ejento.somposigorta.com.tr/dashboard",
  "screenshot": "logs/sompo_after_login.png"
}
```

#### Hata Yanıtı Örneği

```json
{
  "ok": false,
  "error": "Timeout exceeded",
  "screenshot": "logs/sompo_LOGIN_ERROR.png"
}
```

## 🔄 Nasıl Çalışır?

1. **Login URL'ye Git**: `.env` dosyasındaki `SOMPO_LOGIN_URL` adresine gider
2. **Kimlik Bilgileri**: Kullanıcı adı ve şifreyi otomatik doldurur
3. **Google Authenticator**: TOTP secret key kullanarak 6 haneli kodu üretir ve girer
4. **Oturum Kaydet**: Başarılı girişten sonra cookies'leri `storage/cookies/sompo.json` dosyasına kaydeder
5. **Ekran Görüntüsü**: İşlem sonunda ekran görüntüsü alır (`logs/` klasörüne)

## 🛠️ Teknolojiler

- **Python 3.11+**
- **FastAPI**: Modern REST API framework
- **Playwright**: Browser automation
- **pyotp**: Google Authenticator (TOTP) kod üretimi
- **Uvicorn**: ASGI server

## 📌 Notlar

- ⚠️ Browser headless=False modda çalışır (işlemleri görebilirsiniz)
- ⚠️ Google Authenticator secret key'i Base32 formatında olmalı
- ✅ Cookies kaydedilir, sonraki işlemler için kullanılabilir
- ✅ Hata durumunda ekran görüntüsü otomatik alınır

## 🔐 Güvenlik

- `.env` dosyasını **asla** Git'e commit etmeyin
- `storage/cookies/` klasörünü `.gitignore`'a ekleyin
- Hassas bilgileri saklamak için environment variables kullanın

