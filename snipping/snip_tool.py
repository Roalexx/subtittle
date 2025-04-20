from PyQt5.QtWidgets import QApplication, QRubberBand, QWidget
from PyQt5.QtCore import QRect, QPoint, Qt, QSize, QEventLoop, pyqtSignal
from PyQt5.QtGui import QGuiApplication, QPainter, QColor


class SnipTool(QWidget):
    selection_done = pyqtSignal()  # Özel sinyal

    def __init__(self):
        super().__init__()
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()
        self.selected_rect = None

    def mousePressEvent(self, event):
        self.origin = self.mapToGlobal(event.pos())
        self.rubberBand.setGeometry(QRect(event.pos(), QSize()))
        self.rubberBand.show()

    def mouseMoveEvent(self, event):
        current = event.pos()
        self.rubberBand.setGeometry(
            QRect(self.origin - self.mapToGlobal(QPoint(0, 0)), current).normalized())

    def mouseReleaseEvent(self, event):
        end = self.mapToGlobal(event.pos())
        self.selected_rect = QRect(self.origin, end).normalized()
        print("Seçilen gerçek bölge:", self.selected_rect)
        self.selection_done.emit()
        self.close()


def get_selected_screen_region():
    snipper = SnipTool()

    screens = QGuiApplication.screens()
    virtual_rect = screens[0].geometry()
    for screen in screens[1:]:
        virtual_rect = virtual_rect.united(screen.geometry())

    snipper.setWindowOpacity(0.3)
    snipper.setWindowFlags(snipper.windowFlags() |
                           Qt.FramelessWindowHint |
                           Qt.WindowStaysOnTopHint)
    snipper.setGeometry(virtual_rect)

    snipper.show()

    loop = QEventLoop()
    snipper.selection_done.connect(loop.quit)
    loop.exec_()

    return snipper.selected_rect


class PointSelector(QWidget):
    selection_done = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.selected_point = None

        screens = QGuiApplication.screens()
        virtual_geometry = screens[0].geometry()
        for screen in screens[1:]:
            virtual_geometry = virtual_geometry.united(screen.geometry())

        self.setGeometry(virtual_geometry)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setCursor(Qt.CrossCursor)
        self.setMouseTracking(True)
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(100, 100, 100, 100))  

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = self.mapToGlobal(event.pos())
            self.selected_point = (pos.x(), pos.y())
            print("Seçilen Nokta:", self.selected_point)
            self.selection_done.emit()
            self.close()


def get_selected_point():
    selector = PointSelector()
    loop = QEventLoop()
    selector.selection_done.connect(loop.quit)
    loop.exec_()
    return selector.selected_point



