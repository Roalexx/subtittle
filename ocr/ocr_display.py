import sys
import os
import pytesseract
from ocr_display import display_subtitles_on_screen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from snipping.snip_tool import get_selected_screen_region  
from PIL import Image
import mss
import time
from dotenv import load_dotenv

load_dotenv()

# Tesseract yolu
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Snip Tool'dan bölge seç
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

with mss.mss() as sct:
    while True:
        # Ekran görüntüsü al
        screenshot = sct.grab(region)
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

        # OCR ile metni al
        current_text = pytesseract.image_to_string(img, lang='eng').strip()

        print(f"OCR Metni: {current_text}")  # OCR çıktısını kontrol et

        # Metin değiştiyse sadece o zaman yaz ve çevir
        if current_text and current_text != previous_text:
            print("\n📝 Yeni Altyazı:")
            print(current_text)

            # Altyazıyı ekranda göster
            display_subtitles_on_screen(current_text, region)

            previous_text = current_text  # Geçerli metni kaydedelim

        time.sleep(1)  # OCR işlemi 1 saniye aralıklarla yapılacak
