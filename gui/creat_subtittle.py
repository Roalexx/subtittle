import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import win32api
import win32con
import win32gui

_window_ref = None
_app_ref = None

def create_transparent_window(text, position, background_color, text_color, font_size, opacity):
    global _window_ref, _app_ref

    class TransparentWindow(QtWidgets.QLabel):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("SubtitleWindow")
            self.setWindowFlags(
                QtCore.Qt.FramelessWindowHint |
                QtCore.Qt.WindowStaysOnTopHint |
                QtCore.Qt.Tool
            )
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

            # Yazı ve stil
            self.setText(text)
            self.setStyleSheet(
                f"""
                QLabel {{
                    color: {text_color};
                    font-size: {font_size}pt;
                    padding: 10px;
                }}
                """
            )
            self.setWordWrap(True)
            self.setAlignment(QtCore.Qt.AlignCenter)
            self.setFixedWidth(720)
            self.adjustSize()

            self.move(position[0], position[1])

            # Opaklık efekti
            opacity_effect = QtWidgets.QGraphicsOpacityEffect()
            opacity_effect.setOpacity(opacity)
            self.setGraphicsEffect(opacity_effect)

        def paintEvent(self, event):
            painter = QtGui.QPainter(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            rect = self.rect()
            bg_color = QtGui.QColor(background_color)
            bg_color.setAlphaF(opacity)
            painter.setBrush(bg_color)
            painter.setPen(QtCore.Qt.NoPen)
            painter.drawRoundedRect(rect, 15, 15)
            super().paintEvent(event)

        def closeEvent(self, event):
            global _window_ref
            _window_ref = None
            event.accept()

    # QApplication zaten varsa tekrar oluşturma
    if not QtWidgets.QApplication.instance():
        _app_ref = QtWidgets.QApplication(sys.argv)

    # Önceki pencereyi kapat
    if _window_ref:
        _window_ref.close()

    # Yeni pencere oluştur
    _window_ref = TransparentWindow()
    _window_ref.show()

    # Event loop'a girmeden sadece pencereyi canlı tut
    QtCore.QTimer.singleShot(10, lambda: None)
    QtWidgets.QApplication.processEvents()
