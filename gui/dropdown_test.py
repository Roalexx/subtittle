import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QLabel, QPushButton
import win32gui
import win32ui
from PIL import Image
import ctypes
import win32con

def list_open_windows():
    def enum_callback(hwnd, window_list):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                window_list.append((hwnd, title))
    windows = []
    win32gui.EnumWindows(enum_callback, windows)
    return windows

def capture_window(hwnd):
    left, top, right, bottom = win32gui.GetClientRect(hwnd)
    width = right - left
    height = bottom - top

    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()

    save_bitmap = win32ui.CreateBitmap()
    save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
    save_dc.SelectObject(save_bitmap)

    # PrintWindow burada ctypes ile çağrıldı
    result = ctypes.windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 1)

    bmpinfo = save_bitmap.GetInfo()
    bmpstr = save_bitmap.GetBitmapBits(True)

    win32gui.DeleteObject(save_bitmap.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_dc)

    if result == 1:
        image = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)
        return image
    else:
        return None
class WindowSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Açık Pencere Seçici")
        self.setGeometry(200, 200, 400, 150)

        layout = QVBoxLayout()

        self.combo = QComboBox()
        self.windows = list_open_windows()

        for hwnd, title in self.windows:
            self.combo.addItem(title, hwnd)

        layout.addWidget(QLabel("Bir pencere seçin:"))
        layout.addWidget(self.combo)

        self.capture_btn = QPushButton("Ekran Görüntüsünü Al")
        self.capture_btn.clicked.connect(self.capture_selected_window)
        layout.addWidget(self.capture_btn)

        self.setLayout(layout)

    def capture_selected_window(self):
        index = self.combo.currentIndex()
        hwnd = self.combo.itemData(index)
        title = self.combo.currentText()
        print(f"Seçilen pencere: {title} (HWND: {hwnd})")

        img = capture_window(hwnd)
        if img:
            img.save("pencere_ekran_goruntusu.png")
            print("Görüntü başarıyla kaydedildi.")
        else:
            print("Görüntü alınamadı.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    selector = WindowSelector()
    selector.show()
    sys.exit(app.exec_())
