import sys
import os
import tkinter as tk
from tkinter import messagebox, ttk
import threading
import subprocess
import base64
from multiprocessing import freeze_support

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import ocr.ocr_loop as ocr_loop
from snipping.snip_tool import get_selected_point

ocr_running = False
ocr_region = None
display_region = None
subtitle_process = None

# Global ayarlar
background_color = "black"
text_color = "white"
font_size = 18
opacity = 0.8

def show_subtitle(text, position, bg, color, size, opacity):
    global subtitle_process

    # Önceki altyazı varsa kapat
    if subtitle_process and subtitle_process.poll() is None:
        subtitle_process.terminate()

    encoded_text = base64.b64encode(text.encode('utf-8')).decode('utf-8')
    script_path = "gui/subtitle_worker.py"

    subtitle_process = subprocess.Popen([
        sys.executable,
        script_path,
        "--text", encoded_text,
        "--x", str(position[0]),
        "--y", str(position[1]),
        "--bg", bg,
        "--color", color,
        "--size", str(size),
        "--opacity", str(opacity)
    ])

def start_ocr():
    global ocr_running, ocr_region, display_region
    if not ocr_running:
        show_alert()
        ocr_region = ocr_loop.get_region_from_screen()
        if ocr_region is None:
            return
        display_region = get_selected_point()
        if display_region is None:
            return

        ocr_gen = ocr_loop.ocr_loop(ocr_region)
        ocr_running = True

        def run_ocr():
            for translated_text in ocr_gen:
                if not ocr_running:
                    break
                show_subtitle(
                    text=translated_text,
                    position=display_region,
                    bg=background_color,
                    color=text_color,
                    size=font_size,
                    opacity=opacity
                )

        threading.Thread(target=run_ocr, daemon=True).start()

def stop_ocr():
    global ocr_running
    ocr_running = False

def show_alert():
    messagebox.showinfo("Bölge Seçimi", "Önce OCR bölgesini, sonra altyazının çıkacağı yeri seç.")

def main_gui():
    global background_color, text_color, font_size, opacity

    root = tk.Tk()
    root.title("Altyazı Ayarları")

    tk.Label(root, text="Background Color:").pack()
    bg_entry = tk.Entry(root)
    bg_entry.insert(0, background_color)
    bg_entry.pack()

    tk.Label(root, text="Text Color:").pack()
    tc_entry = tk.Entry(root)
    tc_entry.insert(0, text_color)
    tc_entry.pack()

    tk.Label(root, text="Font Size:").pack()
    font_entry = tk.Entry(root)
    font_entry.insert(0, str(font_size))
    font_entry.pack()

    tk.Label(root, text="Opacity:").pack()
    opacity_dropdown = ttk.Combobox(root, values=[round(x * 0.1, 1) for x in range(1, 11)])
    opacity_dropdown.set(str(opacity))
    opacity_dropdown.pack()

    def apply_settings():
        global background_color, text_color, font_size, opacity
        try:
            font_size = int(font_entry.get())
            opacity = float(opacity_dropdown.get())
        except ValueError:
            messagebox.showerror("Hata", "Lütfen geçerli değerler girin.")
            return
        background_color = bg_entry.get()
        text_color = tc_entry.get()
        messagebox.showinfo("Başarılı", "Ayarlar kaydedildi.")

    tk.Button(root, text="Ayarları Uygula", command=apply_settings).pack(pady=5)
    tk.Button(root, text="Başlat", command=start_ocr).pack(pady=10)
    tk.Button(root, text="Durdur", command=stop_ocr).pack(pady=10)

    root.mainloop()

if __name__ == '__main__':
    freeze_support()
    main_gui()
