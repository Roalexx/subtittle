import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytesseract
from snipping.snip_tool import get_selected_screen_region
from PIL import Image
import mss

# Tesseract yolu
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Alan seçtir
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

print("Seçilen bölge:", region)

# mss ile ekran görüntüsü al
with mss.mss() as sct:
    screenshot = sct.grab(region)
    img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
    img.save("debug_test_capture.png")
    print("Görüntü kaydedildi: debug_test_capture.png")

    text = pytesseract.image_to_string(img, lang='eng')
    print("OCR Çıktısı:")
    print(repr(text))
