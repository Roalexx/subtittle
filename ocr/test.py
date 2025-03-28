import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytesseract
import pyautogui
from snipping.snip_tool import get_selected_screen_region
from PIL import Image

# Tesseract yolu
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Bölge seçtir
rect = get_selected_screen_region()
if rect is None:
    print("Hiçbir alan seçilmedi.")
    sys.exit()

region = (rect.x(), rect.y(), rect.width(), rect.height())
print("Seçilen bölge:", region)

# Görüntüyü al ve kaydet
screenshot = pyautogui.screenshot(region=region)
screenshot.save("debug_test_capture.png")
print("Ekran görüntüsü alındı ve debug_test_capture.png olarak kaydedildi.")

# OCR işlemi yap
text = pytesseract.image_to_string(screenshot, lang='eng')
print("OCR çıktısı:")
print(repr(text))
