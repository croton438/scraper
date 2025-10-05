# 🔐 Konfigürasyon Ayarları

Projenin çalışması için `.env` dosyası oluşturmanız gerekmektedir.

## .env Dosyası Oluşturma

Proje kök dizininde `.env` dosyası oluşturun ve aşağıdaki değerleri ekleyin:

```env
# Sompo Portal Giriş Bilgileri

# Login URL (varsayılan olarak kullanılacak)
SOMPO_LOGIN_URL=https://ejento.somposigorta.com.tr/dashboard/login

# Kullanıcı Adı
SOMPO_USER=kullanici_adiniz

# Şifre
SOMPO_PASS=sifreniz

# Google Authenticator Secret Key (TOTP)
# Not: Bu, Google Authenticator'da QR kod okuttuğunuzda aldığınız secret key'dir
# Örnek: JBSWY3DPEHPK3PXP
SOMPO_TOTP_SECRET=your_totp_secret_key_here
```

## Google Authenticator Secret Key Nasıl Bulunur?

1. Google Authenticator'ı açın
2. Sompo için QR kod okuttuğunuzda, genellikle ekranda bir **secret key** (gizli anahtar) gösterilir
3. Bu key genellikle `JBSWY3DPEHPK3PXP` gibi büyük harflerden oluşur
4. Bu key'i `SOMPO_TOTP_SECRET` değişkenine yazın

## Güvenlik Notu

⚠️ `.env` dosyasını asla Git'e commit etmeyin! Bu dosya gizli bilgiler içerir.

