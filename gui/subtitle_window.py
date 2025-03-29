import sys
import threading
from queue import Queue
from PyQt5 import QtWidgets, QtCore, QtGui

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

        self.setStyleSheet("color: white; font-size: 20pt; padding: 10px;")
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setWordWrap(True)
        self.setFixedWidth(800)
        self.move(300, 300)  # Ekrandaki konum
        self.setText("")
        self.show()

        # Arka plan şeffaflığı
        opacity_effect = QtWidgets.QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.9)
        self.setGraphicsEffect(opacity_effect)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        bg_color = QtGui.QColor("black")
        bg_color.setAlphaF(0.8)
        painter.setBrush(bg_color)
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 15, 15)
        super().paintEvent(event)

    def update_text(self, text):
        self.setText(text)
        self.adjustSize()

def listen_to_queue(window, queue):
    while True:
        text = queue.get()
        window.update_text(text)

def launch_subtitle_gui(queue: Queue):
    app = QtWidgets.QApplication(sys.argv)
    window = SubtitleWindow()
    threading.Thread(target=listen_to_queue, args=(window, queue), daemon=True).start()
    app.exec_()

if __name__ == '__main__':
    subtitle_queue = Queue()

    # GUI'yi thread olarak başlat (ana thread'den bağımsız)
    threading.Thread(target=launch_subtitle_gui, args=(subtitle_queue,), daemon=True).start()

    # TEST: 3 saniyede bir yeni altyazı at
    import time
    for t in ["Selam!", "Bir sonraki altyazı", "Son altyazı"]:
        time.sleep(3)
        subtitle_queue.put(t)
