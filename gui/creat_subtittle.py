import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import win32api
import win32con
import win32gui

def create_transparent_window(text, position, background_color, text_color, font_size, opacity):
    class TransparentWindow(QtWidgets.QLabel):
        def __init__(self):
            super().__init__()

            self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

            opacity_effect = QtWidgets.QGraphicsOpacityEffect()
            opacity_effect.setOpacity(opacity)
            self.setGraphicsEffect(opacity_effect)

            self.setText(text)
            self.setStyleSheet(f"color: {text_color}; font-size: {font_size}pt;")
            self.setWordWrap(True)
            self.setMaximumWidth(720)  # Yalnızca maksimum genişliği sınırla

            self.adjustSize()  # Hem genişliği hem yüksekliği içeriğe göre ayarla
            self.move(position[0], position[1])

            QtCore.QTimer.singleShot(100, lambda: self.setWindowTransparent(background_color))  # hwnd bulunmadan önce gecikme

        def setWindowTransparent(self, background_color):
            hwnd = win32gui.FindWindow(None, self.windowTitle())
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                                   win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)

            color = QtGui.QColor(background_color)
            win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(color.red(), color.green(), color.blue()), 0, win32con.LWA_COLORKEY)

        def paintEvent(self, event):
            painter = QtGui.QPainter(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)

            # Dinamik pencere boyutuna uygun arka plan çiz
            color = QtGui.QColor(0, 0, 0, 127)
            painter.setBrush(color)
            painter.setPen(QtCore.Qt.NoPen)
            painter.drawRect(self.rect())

            super().paintEvent(event)

    app = QtWidgets.QApplication(sys.argv)
    window = TransparentWindow()
    window.show()
    sys.exit(app.exec_())

# Test et
create_transparent_window(
    text="Kısa yazı",  # Kısa yazıyla test
    position=(500, 300),
    background_color="black",
    text_color="white",
    font_size=18,
    opacity=0.8
)