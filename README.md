
# 🎮 Subtitle Translator (Real-Time Game Subtitle Translation)

Bu proje, oyunlardaki İngilizce altyazıları otomatik olarak gerçek zamanlı algılar, Türkçeye çevirir ve ekranınızda şeffaf şekilde gösterir. PyQt5 ile özel altyazı penceresi oluşturur.

---

## 🧰 Gereksinimler

- Windows işletim sistemi
- Python 3.10 veya 3.11
- Tesseract OCR
- DeepL API Anahtarı

---

## 🚀 Kurulum ve Çalıştırma

### 1. Projeyi İndir

```bash
git clone git@github.com:Roalexx/subtittle.git
cd subtittle
```

### 2. Virtual Environment (venv) Kur

```bash
python -m venv venv
```

### 3. Ortamı Aktif Et

Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

### 4. Gereksinimleri Yükle

```bash
pip install -r requirements.txt
```

---

## 🧠 Ek Kurulumlar

### 🔤 Tesseract OCR Kurulumu

1. [Tesseract Setup (Windows)](https://github.com/tesseract-ocr/tesseract/wiki)
2. Kurulumdan sonra şu yola dikkat et:  
   `C:\Program Files\Tesseract-OCR\tesseract.exe`

### 🔑 DeepL API Anahtarı

1. [DeepL Developer Portal](https://www.deepl.com/pro#developer) sayfasına gidin
2. Ücretsiz API anahtarınızı alın
3. Proje dizinine `.env` dosyası oluşturun:

```env
DEEPL_API_KEY=buraya_senin_anahtarın
```

---

## ▶️ Projeyi Çalıştırma

```bash
python main.py
```

Açılan pencereden:
- Renk, boyut ve opaklık ayarlarını yap
- “Başlat” butonuna bas
- OCR bölgesini seç
- Altyazının gösterileceği noktayı seç

Hepsi bu 🎉

---

## 📦 Uygulama Oluşturma (.exe)

### 1. PyInstaller Kur

```bash
pip install pyinstaller
```

### 2. Derle

```bash
pyinstaller --noconsole --onefile --add-data ".env;." main.py
```

### 3. Çalıştır

`dist/main.exe` dosyasını çift tıklayarak çalıştırabilirsin.

---

## 📝 Notlar

- Çoklu monitör desteklenir, OCR seçim ekranı ikinci monitörde de çalışır.
- Alt yazılar 10 saniye boyunca gösterilir ve sonra otomatik kapanır.

---

## 📬 Sorular / Katkı

Her türlü katkıya ve geri bildirime açığız.  
Sorular için GitHub Issues kısmını kullanabilirsin.

---

**Hazırlayan:** Roalexx  
**Proje:** Subtitle Real-time Translation Overlay  


🎮 Subtitle Translator (Real-Time Game Subtitle Translation)

This project automatically detects English subtitles in games in real time, translates them into Turkish, and displays them transparently on your screen. It uses PyQt5 to create a custom subtitle window.

---

🧰 Requirements

- Windows operating system
- Python 3.10 or 3.11
- Tesseract OCR
- DeepL API Key

---

🚀 Installation & Run

1. Clone the Project

git clone git@github.com:Roalexx/subtittle.git
cd subtittle

2. Create a Virtual Environment

python -m venv venv

3. Activate the Environment

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

4. Install Requirements

pip install -r requirements.txt

---

🧠 Additional Setup

🔤 Tesseract OCR Installation

1. Go to https://github.com/tesseract-ocr/tesseract/wiki
2. After installation, note this path:
   C:\Program Files\Tesseract-OCR\tesseract.exe

🔑 DeepL API Key

1. Visit https://www.deepl.com/pro#developer
2. Get your free API key
3. Create a .env file in the project root:

DEEPL_API_KEY=your_api_key_here

---

▶️ Running the Project

python main.py

In the window that opens:
- Adjust color, size, and opacity
- Click the “Start” button
- Select the OCR region
- Select where to show the subtitle

That's it 🎉

---

📦 Build as Executable (.exe)

1. Install PyInstaller

pip install pyinstaller

2. Build

pyinstaller --noconsole --onefile --add-data ".env;." main.py

3. Run

Double-click dist/main.exe to run the app.

---

📝 Notes

- Multi-monitor setup is supported. OCR selection works on the second monitor as well.
- Subtitles are shown for 10 seconds and then automatically disappear.

---

📬 Questions / Contributions

We welcome all kinds of contributions and feedback.
For questions, use the GitHub Issues section.

---

Created by: Roalexx
Project: Subtitle Real-time Translation Overlay
