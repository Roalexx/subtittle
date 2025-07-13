import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
import ocr.ocr_loop_test as ocr_loop
from snipping.snip_tool import get_selected_point, get_selected_screen_region  # 🔥 YENİ
from snipping.select_window import list_open_windows
from gui.subtitle_worker import SubtitleWindow

class MainWindow(QtWidgets.QWidget):
    update_subtitle = QtCore.pyqtSignal(str)

    def window_selected(self, index):
        if index > 0:
            self.selected_hwnd = self.window_combo.itemData(index)
            print(f"Seçilen pencere HWND: {self.selected_hwnd}")
        else:
            self.selected_hwnd = None

    def subtitle_window_set_text_safe(self, text):
        if self.subtitle_window:
            self.subtitle_window.set_text(text)

    def __init__(self):
        super().__init__()

        self.ocr_running = False
        self.display_region = None
        self.selected_hwnd = None  # 🔥 YENİ

        self.setWindowTitle("Altyazı Ayarları")
        self.setFixedSize(300, 300)

        self.bg = "black"
        self.text_color = "white"
        self.font_size = 18
        self.opacity = 0.8
        self.subtitle_window = None

        self.init_ui()
        self.update_subtitle.connect(self.subtitle_window_set_text_safe)

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        # Background color
        self.bg_input = QtWidgets.QLineEdit(self.bg)
        layout.addWidget(QtWidgets.QLabel("Background Color:"))
        layout.addWidget(self.bg_input)

        # Text color
        self.tc_input = QtWidgets.QLineEdit(self.text_color)
        layout.addWidget(QtWidgets.QLabel("Text Color:"))
        layout.addWidget(self.tc_input)

        # Font size
        self.font_input = QtWidgets.QLineEdit(str(self.font_size))
        layout.addWidget(QtWidgets.QLabel("Font Size:"))
        layout.addWidget(self.font_input)

        # Opacity
        self.opacity_input = QtWidgets.QComboBox()
        self.opacity_input.addItems([str(round(x * 0.1, 1)) for x in range(1, 11)])
        self.opacity_input.setCurrentText(str(self.opacity))
        layout.addWidget(QtWidgets.QLabel("Opacity:"))
        layout.addWidget(self.opacity_input)

        # Windows
        self.window_combo = QtWidgets.QComboBox()
        self.window_combo.addItem("Bir pencere seçin...")
        self.windows = list_open_windows()
        for hwnd, title in self.windows:
            self.window_combo.addItem(title, hwnd)
        self.window_combo.currentIndexChanged.connect(self.window_selected)
        layout.addWidget(QtWidgets.QLabel("Pencere Seç:"))
        layout.addWidget(self.window_combo)

        # Buttons
        apply_btn = QtWidgets.QPushButton("Ayarları Uygula")
        apply_btn.clicked.connect(self.apply_settings)
        layout.addWidget(apply_btn)

        start_btn = QtWidgets.QPushButton("Başlat")
        start_btn.clicked.connect(self.start_ocr)
        layout.addWidget(start_btn)

        stop_btn = QtWidgets.QPushButton("Durdur")
        stop_btn.clicked.connect(self.stop_ocr)
        layout.addWidget(stop_btn)

        self.setLayout(layout)

    def apply_settings(self):
        try:
            self.font_size = int(self.font_input.text())
            self.opacity = float(self.opacity_input.currentText())
            self.bg = self.bg_input.text()
            self.text_color = self.tc_input.text()
            QtWidgets.QMessageBox.information(self, "Başarılı", "Ayarlar kaydedildi.")
        except ValueError:
            QtWidgets.QMessageBox.critical(self, "Hata", "Geçerli değerler girin.")

    def start_ocr(self):
        if not self.ocr_running:
            if not self.selected_hwnd:
                QtWidgets.QMessageBox.warning(self, "Uyarı", "Lütfen bir pencere seçin.")
                return

            QtWidgets.QMessageBox.information(self, "Alan Seçimi", "Lütfen pencere içinde OCR yapılacak alanı seçin.")
            crop_rect = get_selected_screen_region()  # 🔥 YENİ
            if crop_rect is None:
                return

            self.display_region = get_selected_point()
            if self.display_region is None:
                return

            self.subtitle_window = SubtitleWindow()
            self.subtitle_window.set_text_position((self.display_region[0], self.display_region[1]))
            self.subtitle_window.set_text_prop(self.text_color, self.font_size)
            self.subtitle_window.set_opacity(self.opacity)
            self.subtitle_window._bg_color = self.bg
            self.subtitle_window.show()

            self.ocr_running = True

            def should_continue():
                return self.ocr_running

            def callback(translated_text):
                self.update_subtitle.emit(translated_text)

            def loop():
                ocr_loop.ocr_loop(self.selected_hwnd, crop_rect, should_continue, callback)  # 🔥 YENİ

            QtCore.QThreadPool.globalInstance().start(QtRunnable(loop))

    def stop_ocr(self):
        self.ocr_running = False

class QtRunnable(QtCore.QRunnable):
    def __init__(self, fn):
        super().__init__()
        self.fn = fn

    def run(self):
        self.fn()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
