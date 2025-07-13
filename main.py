import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
import ocr.ocr_loop as ocr_loop
from snipping.snip_tool import get_selected_point
from gui.subtitle_worker import SubtitleWindow
from auth_manager import show_login_dialog, show_register_dialog

class QtRunnable(QtCore.QRunnable):
    def __init__(self, fn):
        super().__init__()
        self.fn = fn
    def run(self):
        self.fn()

class MainWindow(QtWidgets.QWidget):
    update_subtitle = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Subtitle Tool")
        self.setFixedSize(300, 330)
        self.is_logged_in = False
        self.current_user = None
        self.ocr_running = False
        self.ocr_region = None
        self.display_region = None
        self.bg = "black"
        self.text_color = "white"
        self.font_size = 18
        self.opacity = 0.8
        self.subtitle_window = None
        self._build_login_ui()
        self.update_subtitle.connect(self._subtitle_window_set_text_safe)

    def _build_login_ui(self):
        self.login_layout = QtWidgets.QVBoxLayout(self)
        login_btn = QtWidgets.QPushButton("Giriş Yap")
        register_btn = QtWidgets.QPushButton("Kayıt Ol")
        self.login_layout.addWidget(login_btn)
        self.login_layout.addWidget(register_btn)
        login_btn.clicked.connect(self._handle_login)
        register_btn.clicked.connect(self._handle_register)

    def _build_main_ui(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.bg_input = QtWidgets.QLineEdit(self.bg)
        self.tc_input = QtWidgets.QLineEdit(self.text_color)
        self.font_input = QtWidgets.QLineEdit(str(self.font_size))
        self.opacity_input = QtWidgets.QComboBox()
        self.opacity_input.addItems([str(round(x * 0.1, 1)) for x in range(1, 11)])
        self.opacity_input.setCurrentText(str(self.opacity))
        self.main_layout.addWidget(QtWidgets.QLabel("Background Color:"))
        self.main_layout.addWidget(self.bg_input)
        self.main_layout.addWidget(QtWidgets.QLabel("Text Color:"))
        self.main_layout.addWidget(self.tc_input)
        self.main_layout.addWidget(QtWidgets.QLabel("Font Size:"))
        self.main_layout.addWidget(self.font_input)
        self.main_layout.addWidget(QtWidgets.QLabel("Opacity:"))
        self.main_layout.addWidget(self.opacity_input)
        apply_btn = QtWidgets.QPushButton("Ayarları Uygula")
        start_btn = QtWidgets.QPushButton("Başlat")
        stop_btn = QtWidgets.QPushButton("Durdur")
        self.main_layout.addWidget(apply_btn)
        self.main_layout.addWidget(start_btn)
        self.main_layout.addWidget(stop_btn)
        apply_btn.clicked.connect(self.apply_settings)
        start_btn.clicked.connect(self.start_ocr)
        stop_btn.clicked.connect(self.stop_ocr)
        self.login_layout.addLayout(self.main_layout)
        self._toggle_main_controls(False)

    def _toggle_main_controls(self, show):
        for i in range(self.main_layout.count()):
            self.main_layout.itemAt(i).widget().setVisible(show)

    def _handle_login(self):
        user = show_login_dialog(self)
        if user:
            self.current_user = user
            self.is_logged_in = True
            ocr_loop.DEEPL_API_KEY = user.deepl_key
            if not hasattr(self, "main_layout"):
                self._build_main_ui()
            self._toggle_main_controls(True)

    def _handle_register(self):
        if show_register_dialog(self):
            QtWidgets.QMessageBox.information(self, "Bilgi", "Kayıt tamamlandı, giriş yapabilirsiniz.")

    def _subtitle_window_set_text_safe(self, text):
        if self.subtitle_window:
            self.subtitle_window.set_text(text)

    def apply_settings(self):
        try:
            self.font_size = int(self.font_input.text())
            self.opacity = float(self.opacity_input.currentText())
            self.bg = self.bg_input.text()
            self.text_color = self.tc_input.text()
            QtWidgets.QMessageBox.information(self, "OK", "Ayarlar kaydedildi.")
        except ValueError:
            QtWidgets.QMessageBox.critical(self, "Hata", "Geçerli değerler girin.")

    def start_ocr(self):
        if not self.is_logged_in:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Önce giriş yapmalısınız.")
            return
        if self.ocr_running:
            return
        QtWidgets.QMessageBox.information(self, "Bölge", "Önce OCR bölgesini, sonra altyazı konumunu seçin.")
        self.ocr_region = ocr_loop.get_region_from_screen()
        if self.ocr_region is None:
            return
        self.display_region = get_selected_point()
        if self.display_region is None:
            return
        self.subtitle_window = SubtitleWindow()
        self.subtitle_window.set_text_position(tuple(self.display_region[:2]))
        self.subtitle_window.set_text_prop(self.text_color, self.font_size)
        self.subtitle_window.set_opacity(self.opacity)
        self.subtitle_window._bg_color = self.bg
        self.subtitle_window.show()
        self.ocr_running = True
        self._run_ocr_thread()

    def _run_ocr_thread(self):
        def should_continue(): return self.ocr_running
        def callback(t): self.update_subtitle.emit(t)
        def loop(): ocr_loop.ocr_loop(self.ocr_region, should_continue, callback)
        QtCore.QThreadPool.globalInstance().start(QtRunnable(loop))

    def stop_ocr(self):
        self.ocr_running = False

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())