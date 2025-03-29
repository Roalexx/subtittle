import sys
import os
import tkinter as tk
import threading
import time
from tkinter import messagebox
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import ocr.ocr_loop as ocr_loop
from snipping.snip_tool import get_selected_point

ocr_running = False
ocr_region = None
display_region = None

def show_alert():
    messagebox.showinfo("Ekran Bölgesi Seçimi", "Lütfen önce OCR işlemi için bir bölge seçin, ardından metnin gösterileceği bölgeyi seçin.")

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
                
        threading.Thread(target=run_ocr, daemon=True).start()

def stop_ocr():
    global ocr_running
    ocr_running = False    

root = tk.Tk()
root.title("Python Process Controller")

start_button = tk.Button(root, text="Başlat", command=start_ocr)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Durdur", command=stop_ocr)
stop_button.pack(pady=10)

root.mainloop()
