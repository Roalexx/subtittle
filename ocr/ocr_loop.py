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

load_dotenv()

DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

if DEEPL_API_KEY is None:
    print("API Anahtarı bulunamadı! Lütfen .env dosyasına ekleyin.")
    sys.exit()

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# OCR ve çeviri için gerekli fonksiyonları hazırlıyoruz.
def translate_with_deepL(text):
    if text.strip() == "":
        return ""  
    try:
        translator = deepl.Translator(DEEPL_API_KEY)
        result = translator.translate_text(text, target_lang="TR") 
        return result.text
    except deepl.exceptions.AuthorizationException as e:
        print(f"Çeviri hatası: {e}")
        return None

def ocr_loop(region):
    previous_text = ""  
    with mss.mss() as sct:
        while True:
            screenshot = sct.grab(region)
            img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

            current_text = pytesseract.image_to_string(img, lang='eng').strip()

            if current_text != previous_text and current_text != "":
                translated_text = translate_with_deepL(current_text)

                if translated_text:
                    print("Çevrilen Metin:", translated_text)
                    yield translated_text
                else:
                    print("Çeviri yapılamadı.")

                previous_text = current_text

            time.sleep(1)

# OCR alanını almak ve kullanmak için fonksiyon
def get_region_from_screen():
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

    return region

# Ana fonksiyonu dışarıda çağırmak için düzenledik.
if __name__ == "__main__":
    region = get_region_from_screen()
    print("OCR İzleme bölgesi:", region)

    ocr_gen = ocr_loop(region)  # Generator'ı başlatıyoruz
    while True:
        translated_text = next(ocr_gen)  # Her seferinde bir değer alıyoruz
        print("Yeni Çevrilen Metin:", translated_text)
