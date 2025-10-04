# 🚀 Sunucuya Deployment (VDS/VPS)

## ✅ Hazırlık

Kodlarınız hazır! Sompo portal'ı IP bazlı erişim kontrolü yaptığı için sunucunuzdan çalıştırmanız gerekiyor.

---

## 📦 1. Dosyaları Sunucuya Yükle

### Git ile (Önerilen)
```bash
# Sunucuda
cd /var/www/
git clone https://github.com/your-repo/scraper.git
cd scraper
```

### SCP/FTP ile
```bash
# Local'den sunucuya
scp -r C:\Users\cifci\Desktop\scraper/* root@sunucu-ip:/var/www/scraper/
```

---

## 🐧 2. Sunucuda Kurulum

### Ubuntu/Debian
```bash
# Python ve pip
sudo apt update
sudo apt install python3 python3-pip python3-venv -y

# Playwright dependencies
sudo apt install -y \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2

# Virtual environment
cd /var/www/scraper
python3 -m venv venv
source venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Playwright browser yükle
playwright install chromium
playwright install-deps chromium
```

---

## 🔐 3. .env Dosyası Oluştur

```bash
cat > .env << 'EOF'
SOMPO_USER=BULUT1
SOMPO_PASS=EEsigorta..28
SOMPO_TOTP_SECRET=DD3JCJB7E7H25MB6BZ5IKXLKLJBZDQAO
SOMPO_LOGIN_URL=https://ejento.somposigorta.com.tr/dashboard/login
HEADLESS=true
API_HOST=0.0.0.0
API_PORT=8000
EOF
```

---

## 🧪 4. Test Et

### Basit Login Testi
```bash
source venv/bin/activate
python test_login.py
```

### API Test
```bash
# Terminal 1: API başlat
python main.py

# Terminal 2: Test et
curl http://localhost:8000/health
curl -X POST http://localhost:8000/sompo/login
```

---

## 🔄 5. Production Deployment

### Systemd Service (Önerilen)

`/etc/systemd/system/scraper.service` dosyası oluştur:

```ini
[Unit]
Description=Insurance Scraper API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/scraper
Environment="PATH=/var/www/scraper/venv/bin"
ExecStart=/var/www/scraper/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Servisi başlat:
```bash
sudo systemctl daemon-reload
sudo systemctl enable scraper
sudo systemctl start scraper
sudo systemctl status scraper
```

### PM2 ile (Alternatif)
```bash
# PM2 yükle
npm install -g pm2

# API başlat
pm2 start main.py --interpreter python3 --name scraper-api
pm2 save
pm2 startup
```

---

## 🌐 6. Nginx Reverse Proxy (Opsiyonel)

`/etc/nginx/sites-available/scraper` dosyası:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Aktif et:
```bash
sudo ln -s /etc/nginx/sites-available/scraper /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 📊 7. Log Kontrolü

```bash
# Systemd logs
sudo journalctl -u scraper -f

# PM2 logs
pm2 logs scraper-api

# Uygulama logs
tail -f logs/sompo_*.png  # Screenshots
tail -f /var/www/scraper/storage/cookies/sompo.json  # Cookies
```

---

## 🔒 8. Güvenlik

### Firewall Ayarları
```bash
# UFW
sudo ufw allow 8000/tcp
sudo ufw enable

# iptables
sudo iptables -A INPUT -p tcp --dport 8000 -j ACCEPT
```

### .env Dosyası İzinleri
```bash
chmod 600 .env
chown www-data:www-data .env
```

---

## 🧪 9. API Kullanımı (Sunucudan)

### Curl ile Test
```bash
# Health check
curl http://localhost:8000/health

# Sompo login
curl -X POST http://localhost:8000/sompo/login

# Teklif alma
curl -X POST http://localhost:8000/sompo/tamamlayici \
  -H "Content-Type: application/json" \
  -d '{"parameters": {"tc_no": "12345678901"}}'
```

### Python ile Test
```python
import requests

# Login
response = requests.post("http://localhost:8000/sompo/login")
print(response.json())

# Teklif
response = requests.post(
    "http://localhost:8000/sompo/tamamlayici",
    json={"parameters": {"tc_no": "12345678901"}}
)
print(response.json())
```

---

## 🐛 Sorun Giderme

### 1. Playwright Browser Hatası
```bash
# Dependencies tekrar yükle
playwright install-deps chromium

# Manuel test
python -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); b = p.chromium.launch(); print('OK'); b.close(); p.stop()"
```

### 2. Permission Denied
```bash
sudo chown -R www-data:www-data /var/www/scraper
sudo chmod -R 755 /var/www/scraper
```

### 3. Port Already in Use
```bash
# Port'u kullanan process'i bul
sudo lsof -i :8000
sudo kill -9 <PID>
```

### 4. Screenshot Alamıyor
```bash
# logs klasörü oluştur
mkdir -p logs storage/cookies
chmod 755 logs storage/cookies
```

---

## 📝 Hızlı Komutlar

```bash
# Service restart
sudo systemctl restart scraper

# Logs göster
sudo journalctl -u scraper --since "5 minutes ago"

# API test
curl http://localhost:8000/health

# Çerezleri kontrol et
cat storage/cookies/sompo.json

# Screenshot'ları listele
ls -lh logs/
```

---

## ✅ Checklist

- [ ] Python 3.8+ kurulu
- [ ] Virtual environment oluşturuldu
- [ ] `requirements.txt` bağımlılıkları yüklendi
- [ ] Playwright browser yüklendi (`playwright install chromium`)
- [ ] `.env` dosyası oluşturuldu
- [ ] `test_login.py` başarıyla çalıştı
- [ ] API başlatıldı (`python main.py`)
- [ ] Health check başarılı (`curl http://localhost:8000/health`)
- [ ] Sompo login test edildi
- [ ] Systemd service kuruldu (production için)
- [ ] Firewall ayarları yapıldı

---

## 🎯 Beklenen Sonuç

```bash
$ curl -X POST http://localhost:8000/sompo/login

{
  "ok": true,
  "msg": "Sompo login başarılı",
  "url": "https://ejento.somposigorta.com.tr/dashboard",
  "cookies_saved": true
}
```

Başarılar! 🚀

