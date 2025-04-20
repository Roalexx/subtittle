import threading
from PyQt5 import QtWidgets, QtCore, QtGui

def create_transparent_window(text, position, background_color, text_color, font_size, opacity):
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
            self.setStyleSheet(f"color: {text_color}; font-size: {font_size}pt; padding: 10px;")
            self.setWordWrap(True)
            self.setAlignment(QtCore.Qt.AlignCenter)
            self.setFixedWidth(720)
            self.adjustSize()
            self.move(position[0], position[1])
            opacity_effect = QtWidgets.QGraphicsOpacityEffect()
            opacity_effect.setOpacity(opacity)
            self.setGraphicsEffect(opacity_effect)

        def paintEvent(self, event):
            painter = QtGui.QPainter(self)
            bg = QtGui.QColor(background_color)
            bg.setAlphaF(opacity)
            painter.setBrush(bg)
            painter.setPen(QtCore.Qt.NoPen)
            painter.drawRoundedRect(self.rect(), 15, 15)
            super().paintEvent(event)

    def show_window():
        app = QtWidgets.QApplication([])
        window = TransparentWindow()
        window.show()
        QtCore.QTimer.singleShot(10000, app.quit)  # 10 saniye sonra kapat
        app.exec_()

    threading.Thread(target=show_window, daemon=True).start()
