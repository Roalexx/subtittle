from PyQt5.QtWidgets import QApplication, QRubberBand, QWidget
from PyQt5.QtCore import QRect, QPoint, Qt, QSize
from PyQt5.QtGui import QGuiApplication, QPainter, QColor
import sys

class SnipTool(QWidget):
    def mousePressEvent(self, event):
        self.origin = self.mapToGlobal(event.pos())  # global pozisyon
        self.rubberBand.setGeometry(QRect(event.pos(), QSize()))
        self.rubberBand.show()

    def mouseMoveEvent(self, event):
        current = event.pos()
        self.rubberBand.setGeometry(QRect(self.origin - self.mapToGlobal(QPoint(0, 0)), current).normalized())

    def mouseReleaseEvent(self, event):
        end = self.mapToGlobal(event.pos())
        self.selected_rect = QRect(self.origin, end).normalized()
        print("Seçilen gerçek bölge:", self.selected_rect)
        self.close()

def get_selected_screen_region():
    app = QApplication(sys.argv)

    snipper = SnipTool()

    # Tam ekran yap: birleşik ekranlar (negatifler dahil)
    screens = QGuiApplication.screens()
    virtual_rect = screens[0].geometry()
    for screen in screens[1:]:
        virtual_rect = virtual_rect.united(screen.geometry())

    snipper.setWindowOpacity(0.3)
    snipper.setWindowFlags(snipper.windowFlags() |
                           Qt.FramelessWindowHint |
                           Qt.WindowStaysOnTopHint)
    snipper.setGeometry(virtual_rect)

    snipper.rubberBand = QRubberBand(QRubberBand.Rectangle, snipper)
    snipper.origin = QPoint()
    snipper.selected_rect = None

    snipper.show()
    app.exec_()
    return snipper.selected_rect

class PointSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_point = None

        # Tüm ekranları kapsayan birleşik geometri
        screens = QGuiApplication.screens()
        virtual_geometry = screens[0].geometry()
        for screen in screens[1:]:
            virtual_geometry = virtual_geometry.united(screen.geometry())

        self.setGeometry(virtual_geometry)

        # Pencere ayarları
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setCursor(Qt.CrossCursor)
        self.setMouseTracking(True)
        self.show()

    def paintEvent(self, event):
        # Yarı saydam gri arka plan çizimi
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(100, 100, 100, 100))  # gri & %40 opak

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = self.mapToGlobal(event.pos())
            self.selected_point = (pos.x(), pos.y())
            print("Seçilen Nokta:", self.selected_point)
            self.close()

def get_selected_point():
    app = QApplication(sys.argv)
    selector = PointSelector()
    app.exec_()
    return selector.selected_point
if __name__ == "__main__":
    point = get_selected_screen_region()
    print("Kullanıcının seçtiği nokta:", point)