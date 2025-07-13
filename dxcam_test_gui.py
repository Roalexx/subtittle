# dxcam_gui_test.py

import sys
from PyQt5 import QtWidgets, QtCore
from snipping.select_window import list_open_windows
from snipping.snip_tool import get_selected_screen_region
import dxcam
from PIL import Image
import numpy as np

class DxcamTestWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dxcam GUI Test")
        self.setFixedSize(350, 300)

        self.selected_hwnd = None
        self.selected_region = None

        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        self.window_combo = QtWidgets.QComboBox()
        self.window_combo.addItem("Bir pencere seçin...")
        self.windows = list_open_windows()
        for hwnd, title in self.windows:
            self.window_combo.addItem(title, hwnd)
        self.window_combo.currentIndexChanged.connect(self.window_selected)

        layout.addWidget(QtWidgets.QLabel("Pencere Seç:"))
        layout.addWidget(self.window_combo)

        select_region_btn = QtWidgets.QPushButton("Ekran Alanı Seç")
        select_region_btn.clicked.connect(self.select_region)
        layout.addWidget(select_region_btn)

        capture_btn = QtWidgets.QPushButton("Görüntüyü Al ve Kaydet")
        capture_btn.clicked.connect(self.capture_with_dxcam)
        layout.addWidget(capture_btn)

        self.setLayout(layout)

    def window_selected(self, index):
        if index > 0:
            self.selected_hwnd = self.window_combo.itemData(index)
            print(f"✅ Seçilen HWND: {self.selected_hwnd}")
        else:
            self.selected_hwnd = None

    def select_region(self):
        region = get_selected_screen_region()
        if region:
            self.selected_region = (
                region.x(),
                region.y(),
                region.x() + region.width(),
                region.y() + region.height()
            )
            print(f"📸 Seçilen Bölge: {self.selected_region}")

    def capture_with_dxcam(self):
        if self.selected_region is None:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Lütfen önce bir alan seçin.")
            return

        print("🎥 Görüntü alınıyor...")
        camera = dxcam.create(output_color="RGB", adapter_idx=0)
        frame = camera.grab(region=self.selected_region)

        if frame is not None:
            img = Image.fromarray(frame)
            img.save("dxcam_capture.png")
            QtWidgets.QMessageBox.information(self, "Başarılı", "Görüntü dxcam_capture.png olarak kaydedildi.")
        else:
            QtWidgets.QMessageBox.critical(self, "Hata", "Görüntü alınamadı.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DxcamTestWindow()
    window.show()
    sys.exit(app.exec_())
