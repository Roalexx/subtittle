import ctypes
import time
import pytesseract
from PIL import Image
import win32gui
import win32ui
from PyQt5.QtCore import QRect
import deepl
import os
from dotenv import load_dotenv

# Load environment (.env) for DeepL key
load_dotenv()
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if DEEPL_API_KEY is None:
    print("❌ DeepL API anahtarı bulunamadı! .env dosyasına DEEPL_API_KEY ekleyin.")
    exit()

def translate_with_deepL(text):
    if not text.strip():
        return ""
    try:
        translator = deepl.Translator(DEEPL_API_KEY)
        result = translator.translate_text(text, target_lang="TR")
        return result.text
    except Exception as e:
        print("Çeviri hatası:", e)
        return ""

def capture_hwnd(hwnd):
    left, top, right, bottom = win32gui.GetClientRect(hwnd)
    width = right - left
    height = bottom - top

    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()

    save_bitmap = win32ui.CreateBitmap()
    save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
    save_dc.SelectObject(save_bitmap)

    ctypes.windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 1)

    bmpinfo = save_bitmap.GetInfo()
    bmpstr = save_bitmap.GetBitmapBits(True)

    win32gui.DeleteObject(save_bitmap.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_dc)

    return Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                            bmpstr, 'raw', 'BGRX', 0, 1)

def map_to_window_coords(hwnd, global_rect: QRect):
    win_left, win_top, _, _ = win32gui.GetWindowRect(hwnd)
    x = global_rect.x() - win_left
    y = global_rect.y() - win_top
    return x, y, global_rect.width(), global_rect.height()

def ocr_loop(hwnd, crop_rect, should_continue, callback):
    previous_text = ""
    x, y, w, h = map_to_window_coords(hwnd, crop_rect)

    while should_continue():
        try:
            image = capture_hwnd(hwnd)
            cropped = image.crop((x, y, x + w, y + h))

            current_text = pytesseract.image_to_string(cropped, lang='eng').strip()
            print("OCR:", current_text)

            if current_text and current_text != previous_text:
                translated = translate_with_deepL(current_text)
                if translated:
                    print("Çeviri:", translated)
                    callback(translated)
                previous_text = current_text

        except Exception as e:
            print(f"OCR sırasında hata oluştu: {e}")

        time.sleep(3)
