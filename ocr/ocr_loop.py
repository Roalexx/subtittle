import sys, os, time, deepl, pytesseract, mss
from PIL import Image
from snipping.snip_tool import get_selected_screen_region

DEEPL_API_KEY = None
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def translate_with_deepL(text: str) -> str | None:
    if not text.strip():
        return ""
    if DEEPL_API_KEY is None:
        return None
    try:
        translator = deepl.Translator(DEEPL_API_KEY)
        return translator.translate_text(text, target_lang="TR").text
    except deepl.exceptions.AuthorizationException:
        return None

def ocr_loop(region: dict, should_continue, callback):
    previous_text = ""
    with mss.mss() as sct:
        while should_continue():
            img = Image.frombytes("RGB", sct.grab(region).size, sct.grab(region).rgb)
            current_text = pytesseract.image_to_string(img, lang='eng').strip()
            if current_text and current_text != previous_text:
                translated = translate_with_deepL(current_text)
                if translated:
                    callback(translated)
                previous_text = current_text
            time.sleep(3)

def get_region_from_screen() -> dict | None:
    rect = get_selected_screen_region()
    if rect is None:
        return None
    return {"top": rect.y(), "left": rect.x(), "width": rect.width(), "height": rect.height()}

if __name__ == "__main__":
    region = get_region_from_screen()
    if region:
        ocr_loop(region, lambda: True, print)