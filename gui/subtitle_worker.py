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
        self.setWordWrap(True)
        self.setFixedWidth(720)
        self._bg_color = "red"
        self.adjustSize()

        self.hide_timer = QtCore.QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.hide)

    def set_text_prop(self, text_color, font_size):
        self.setStyleSheet(f"color: {text_color}; font-size: {font_size}pt; padding: 10px;")

    def set_text_position(self, position):
        self.move(position[0], position[1])
    
    def set_opacity(self, opacity):
        opacity_effect = QtWidgets.QGraphicsOpacityEffect()
        opacity_effect.setOpacity(opacity)
        self.setGraphicsEffect(opacity_effect)

    def set_text(self, text):
        self.setText(text)
        self.adjustSize()

        self.show()  
        self.hide_timer.start(3000)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        bg_color = QtGui.QColor(self._bg_color)
        bg_color.setAlphaF(0.5)
        painter.setBrush(bg_color)
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 15, 15)
        super().paintEvent(event)
