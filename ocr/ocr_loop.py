import sys
import os
import requests
import deepl
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytesseract
from snipping.snip_tool import get_selected_screen_region
from PIL import Image
import mss
import time
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# DeepL API Key (şimdi .env dosyasından alınıyor)
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

# Anahtarın doğru şekilde alındığını kontrol et
if DEEPL_API_KEY is None:
    print("API Anahtarı bulunamadı! Lütfen .env dosyasına ekleyin.")
    sys.exit()

# Tesseract yolu
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Alan seç
rect = get_selected_screen_region()
if rect is None:
    print("Hiçbir alan seçilmedi.")
    sys.exit()

region = {
    "top": rect.y(),
    "left": rect.x(),
    "width": rect.width(),
    "height": rect.height()
}

print("OCR İzleme bölgesi:", region)

# İlk önceki metin boş başlasın
previous_text = ""

# DeepL Çeviri fonksiyonu
def translate_with_deepL(text):
    try:
        translator = deepl.Translator(DEEPL_API_KEY)
        result = translator.translate_text(text, target_lang="TR")  # Dili TR olarak değiştirdik
        return result.text
    except deepl.exceptions.AuthorizationException as e:
        print(f"Çeviri hatası: {e}")
        return None

with mss.mss() as sct:
    while True:
        # Ekran görüntüsü al
        screenshot = sct.grab(region)
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

        # OCR ile metni al
        current_text = pytesseract.image_to_string(img, lang='eng').strip()

        # OCR Metni değişmediyse ekrana tekrar yazdırma
        if current_text != previous_text:
            print("\n📝 Yeni Altyazı:")
            print(current_text)

            # Çeviriyi DeepL ile yap
            translated_text = translate_with_deepL(current_text)

            if translated_text:
                print("🌍 Çeviri (DeepL):")
                print(translated_text)
            else:
                print("Çeviri yapılamadı.")

            # Geçerli metni kaydet
            previous_text = current_text

        time.sleep(1)  # OCR işlemi 1 saniye aralıklarla yapılacak
