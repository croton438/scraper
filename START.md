# 🚀 Sompo Sigorta - Hızlı Başlangıç

## ✅ Sistem Hazır!

Gerçek Sompo portal bilgileri ile kod güncellendi:
- URL: https://ejento.somposigorta.com.tr/dashboard/login
- Username: BULUT1
- Password: EEsigorta..28
- TOTP Secret: DD3JCJB7E7H25MB6BZ5IKXLKLJBZDQAO

---

## 📋 ADIM 1: .env Dosyası Oluştur

Kök dizinde `.env` dosyası oluşturun ve şunu ekleyin:

```env
SOMPO_USER=BULUT1
SOMPO_PASS=EEsigorta..28
SOMPO_TOTP_SECRET=DD3JCJB7E7H25MB6BZ5IKXLKLJBZDQAO
SOMPO_LOGIN_URL=https://ejento.somposigorta.com.tr/dashboard/login
HEADLESS=false
```

**Windows PowerShell'de:**
```powershell
@"
SOMPO_USER=BULUT1
SOMPO_PASS=EEsigorta..28
SOMPO_TOTP_SECRET=DD3JCJB7E7H25MB6BZ5IKXLKLJBZDQAO
SOMPO_LOGIN_URL=https://ejento.somposigorta.com.tr/dashboard/login
HEADLESS=false
"@ | Out-File -FilePath .env -Encoding utf8
```

---

## 📦 ADIM 2: Bağımlılıkları Yükle

```powershell
# Virtual environment aktif et (eğer yoksa oluştur)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Bağımlılıkları yükle
pip install -r requirements.txt

# Playwright browser yükle
playwright install chromium
```

---

## 🎯 ADIM 3: API'yi Çalıştır

```powershell
python main.py
```

API başlatıldı:
- **Swagger UI**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 🧪 ADIM 4: Login Testi

### Yöntem 1: Swagger UI (Tavsiye Edilen)

1. http://localhost:8000/docs adresini aç
2. `POST /sompo/login` endpoint'ini genişlet
3. "Try it out" butonuna tıkla
4. "Execute" butonuna tıkla

### Yöntem 2: PowerShell

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/sompo/login" -Method POST
```

### Yöntem 3: curl (Git Bash varsa)

```bash
curl -X POST http://localhost:8000/sompo/login
```

---

## 📸 Screenshot'lar

Login sırasında otomatik screenshot'lar alınır:

```
logs/
├── sompo_01_login_page.png          # Login sayfası
├── sompo_02_credentials_filled.png  # Kullanıcı adı/şifre girildi
├── sompo_03_totp_filled.png         # 2FA kodu girildi
└── sompo_04_after_login.png         # Dashboard (login başarılı)
```

---

## 🍪 Çerez Yönetimi

Login başarılı olursa çerezler otomatik kaydedilir:

```
storage/cookies/sompo.json
```

İkinci login denemesinde çerezler yüklenir, tekrar giriş gerekmez.

---

## 📋 ADIM 5: Teklif Testi

Login sonrası teklif almayı deneyin:

```powershell
$body = @{
    parameters = @{
        tc_no = "12345678901"
        dogum_tarihi = "1990-01-01"
    }
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/sompo/tamamlayici" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

---

## 🔍 Özellikler

### ✅ Login Fonksiyonu

- 🔄 Otomatik selector tespiti (10+ farklı selector denenir)
- 🔐 TOTP (Google Authenticator) desteği
- 🍪 Çerez kaydetme/yükleme
- 📸 Her adımda screenshot
- ⚠️ Detaylı hata mesajları

### ✅ Teklif Fonksiyonu

- 🔄 Çerez kontrolü (login yoksa otomatik login)
- 🔍 Menü bulma (text, href, class selector'ları)
- 📸 Her adımda screenshot
- 📝 Form alanı tespiti (hazır altyapı)

---

## 🐛 Hata Çözümleri

### 1. "Username input bulunamadı"

Gerçek portal selector'ı farklı olabilir. `logs/sompo_01_login_page.png` dosyasına bakın.

**Çözüm:** `portals/sompo.py` dosyasındaki selector listesine ekleyin.

### 2. "TOTP secret .env dosyasında tanımlı değil"

`.env` dosyasında `SOMPO_TOTP_SECRET` satırını kontrol edin.

### 3. "Browser başlatılamadı"

```powershell
playwright install chromium --force
```

### 4. Headless modda çalışmıyor

`.env` dosyasında:
```env
HEADLESS=false
```

---

## 📊 Beklenen Çıktı

### Login Başarılı:

```json
{
  "ok": true,
  "msg": "Sompo login başarılı",
  "url": "https://ejento.somposigorta.com.tr/dashboard",
  "cookies_saved": true
}
```

### Console Log:

```
🔗 Login URL'e gidiliyor: https://ejento.somposigorta.com.tr/dashboard/login
👤 Username giriliyor: BULUT1
✓ Username selector bulundu: input[type="text"]
🔒 Password giriliyor...
✓ Password selector bulundu: input[type="password"]
🖱️ Login butonuna tıklanıyor...
✓ Login button selector bulundu: button[type="submit"]
🔐 2FA kontrolü yapılıyor...
✓ TOTP input bulundu: input[name="otp"]
🔢 TOTP kodu: 123456
✅ Dashboard yüklenmesi bekleniyor...
✓ Dashboard elementi bulundu: nav
📍 Mevcut URL: https://ejento.somposigorta.com.tr/dashboard
🍪 Çerezler kaydedildi: storage/cookies/sompo.json
```

---

## 🎯 Sonraki Adımlar

1. ✅ Login'i test et
2. ✅ Çerez kaydını kontrol et (`storage/cookies/sompo.json`)
3. ✅ Dashboard screenshot'ını kontrol et (`logs/sompo_04_after_login.png`)
4. ✅ Teklif fonksiyonunu test et
5. 📋 Portal menü yapısına göre selector'ları güncelle

---

## 🔐 Güvenlik Notu

`.env` dosyası `.gitignore`'da olduğu için Git'e push edilmez. ✅

---

Başarılar! 🎉

