#!/bin/bash
# Sunucu Test Script

echo "============================================"
echo "SUNUCU KURULUM VE TEST"
echo "============================================"

# 1. Python kontrolü
echo -e "\n[1] Python versiyonu:"
python3 --version

# 2. Virtual environment
echo -e "\n[2] Virtual environment oluşturuluyor..."
python3 -m venv venv
source venv/bin/activate

# 3. Bağımlılıklar
echo -e "\n[3] Bağımlılıklar yükleniyor..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Playwright
echo -e "\n[4] Playwright browser yükleniyor..."
playwright install chromium
playwright install-deps chromium

# 5. .env kontrolü
echo -e "\n[5] .env dosyası kontrol ediliyor..."
if [ -f .env ]; then
    echo "[OK] .env dosyası mevcut"
else
    echo "[!] .env dosyası oluşturuluyor..."
    cat > .env << 'EOF'
SOMPO_USER=BULUT1
SOMPO_PASS=EEsigorta..28
SOMPO_TOTP_SECRET=DD3JCJB7E7H25MB6BZ5IKXLKLJBZDQAO
SOMPO_LOGIN_URL=https://ejento.somposigorta.com.tr/dashboard/login
HEADLESS=true
EOF
fi

# 6. Klasörler
echo -e "\n[6] Gerekli klasörler oluşturuluyor..."
mkdir -p logs storage/cookies

# 7. Test
echo -e "\n[7] API başlatılıyor..."
echo "[!] API http://localhost:8000 adresinde çalışacak"
echo "[!] CTRL+C ile durdurun"
python main.py

