import sys
import argparse
import base64
from PyQt5 import QtWidgets, QtCore, QtGui

def create_window(text, x, y, background_color, text_color, font_size, opacity):
    class SubtitleWindow(QtWidgets.QLabel):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Subtitle")
            self.setWindowFlags(
                QtCore.Qt.FramelessWindowHint |
                QtCore.Qt.WindowStaysOnTopHint |
                QtCore.Qt.Tool
            )
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

            self.setStyleSheet(f"color: {text_color}; font-size: {font_size}pt; padding: 10px;")
            self.setWordWrap(True)
            self.setFixedWidth(720)

            self.setText(text)
            self.adjustSize()
            self.move(x, y)

            opacity_effect = QtWidgets.QGraphicsOpacityEffect()
            opacity_effect.setOpacity(opacity)
            self.setGraphicsEffect(opacity_effect)

        def paintEvent(self, event):
            painter = QtGui.QPainter(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            bg_color = QtGui.QColor(background_color)
            bg_color.setAlphaF(opacity)
            painter.setBrush(bg_color)
            painter.setPen(QtCore.Qt.NoPen)
            painter.drawRoundedRect(self.rect(), 15, 15)
            super().paintEvent(event)

    app = QtWidgets.QApplication(sys.argv)
    window = SubtitleWindow()
    window.show()
    QtCore.QTimer.singleShot(10000, app.quit)  # 10 saniye sonra pencereyi kapat
    app.exec_()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--x", type=int, required=True)
    parser.add_argument("--y", type=int, required=True)
    parser.add_argument("--bg", default="black")
    parser.add_argument("--color", default="white")
    parser.add_argument("--size", type=int, default=18)
    parser.add_argument("--opacity", type=float, default=0.8)
    args = parser.parse_args()

    decoded_text = base64.b64decode(args.text.encode('utf-8')).decode('utf-8')

    create_window(
        text=decoded_text,
        x=args.x,
        y=args.y,
        background_color=args.bg,
        text_color=args.color,
        font_size=args.size,
        opacity=args.opacity
    )
