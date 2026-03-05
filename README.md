```markdown
# 🤖 AI-Powered Data Assistant (SQL Bot)

Bu proje, doğal dil (Türkçe) sorgularını otomatik olarak MS SQL Server sorgularına dönüştüren ve veritabanından aldığı sonuçları insansı bir dille kullanıcıya sunan bir yapay zeka asistanıdır. LangChain mimarisi ve Google Gemini 2.5 Flash modeli üzerine inşa edilmiştir.



## ✨ Öne Çıkan Özellikler

* **Doğal Dil İşleme:** SQL bilmenize gerek kalmadan "En çok hedefi olan çalışan kim?" gibi sorular sorabilirsiniz.
* **Turbo Mod (Hız Optimizasyonu):** Veritabanı şemasını hafızada (cache) tutarak yanıt süresini %80 oranında hızlandırır.
* **Çift Zincirli Mimari:** Önce doğru SQL'i üretir, ardından sonucu analiz ederek doğal bir Türkçe cevap oluşturur.
* **Güvenli Erişim:** Sadece `SELECT` (okuma) yetkisiyle çalışacak şekilde kısıtlanmıştır.

## 🛠️ Gereksinimler

Sistemi ayağa kaldırmak için aşağıdaki bileşenlerin yüklü olması gerekir:

* **Python:** 3.10 veya üzeri (Testler Python 3.14 ile yapılmıştır).
* **Veritabanı:** MS SQL Server (Express/LocalDB/Standard).
* **Sürücü:** Microsoft ODBC Driver 17 for SQL Server.
* **API Anahtarı:** Google AI Studio üzerinden ücretsiz Gemini API anahtarı.

## 🚀 Kurulum ve Çalıştırma

### 1. Kütüphanelerin Yüklenmesi
Terminal veya PowerShell üzerinden gerekli paketleri kurun:

```bash
pip install langchain langchain-google-genai langchain-community pyodbc sqlalchemy langchain-core

```

### 2. Yapılandırma

`sqlbot.py` dosyasını açın ve aşağıdaki alanları kendi bilgilerinizle güncelleyin:

```python
import os

# API Anahtarınızı girin
os.environ["GOOGLE_API_KEY"] = "AI..."

# Veritabanı bağlantı bilgilerinizi girin
server = r'(localdb)\MSSQLLocalDB'
database = 'bilgi_islem'

```

### 3. Uygulamayı Başlatma

Proje klasöründeyken şu komutu çalıştırın:

```bash
python sqlbot.py

```

## 📋 Örnek Sorgular

Sistem açıldıktan sonra aşağıdaki gibi sorular sorabilirsiniz:

* *"2026 Dönem" adlı dönemde toplam kaç tane hedef tanımlanmış?"*
* *"IT departmanındaki çalışanların listesini getir."*

## ⚠️ Önemli Notlar

* **Hız:** İlk çalıştırmada veritabanı şemasını okuduğu için kısa bir gecikme olabilir, sonraki tüm sorular "Turbo" hızda yanıtlanır.
