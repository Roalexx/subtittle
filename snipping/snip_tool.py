from PyQt5.QtWidgets import QApplication, QRubberBand, QWidget
from PyQt5.QtCore import QRect, QPoint, Qt, QSize
from PyQt5.QtGui import QGuiApplication
import sys

class SnipTool(QWidget):
    def mousePressEvent(self, event):
        self.origin = event.pos()
        self.rubberBand.setGeometry(QRect(self.origin, QSize()))
        self.rubberBand.show()

    def mouseMoveEvent(self, event):
        self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        self.selected_rect = self.rubberBand.geometry()
        self.close()

def get_selected_screen_region():
    app = QApplication(sys.argv)

    snipper = SnipTool()

    # ✅ Gerekli tüm ayarları burada yapıyoruz (init içinde değil)
    snipper.setWindowOpacity(0.3)
    snipper.setWindowFlags(snipper.windowFlags() |
                           Qt.FramelessWindowHint |
                           Qt.WindowStaysOnTopHint)

    # Sadece birincil ekranı kapsasın (siyah ekran engellenir)
    snipper.setGeometry(QGuiApplication.primaryScreen().geometry())

    snipper.rubberBand = QRubberBand(QRubberBand.Rectangle, snipper)
    snipper.origin = QPoint()
    snipper.selected_rect = None

    snipper.show()
    app.exec_()
    return snipper.selected_rect
