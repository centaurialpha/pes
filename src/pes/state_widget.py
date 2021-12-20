from PyQt5.QtWidgets import (
    QWidget,
)
from PyQt5.QtGui import (
    QPainter,
    QColor,
    QPen,
)
from PyQt5.QtCore import (
    QSize,
    Qt,
    QTimer,
    pyqtSignal,
)


class StateWidget(QWidget):
    clicked = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.radius = 8
        self.state = False
        self._clickable = False
        self._line_width = 0
        self.state1_color = QColor("#9d9d9d")
        self.state2_color = QColor("#77dd77")

    @property
    def line_width(self):
        return self._line_width

    @line_width.setter
    def line_width(self, width):
        self._line_width = width

    @property
    def clickable(self):
        return self._clickable

    @clickable.setter
    def clickable(self, value):
        self._clickable = value
        self.setMouseTracking(value)

    def change_state(self):
        self.state = not self.state
        self.update()

    def mousePressEvent(self, event):
        if not self.clickable:
            return
        self.change_state()
        self.clicked.emit()

    def sizeHint(self):
        return QSize(25, 25)

    def minimumSizeHint(self):
        return self.sizeHint()

    def testing(self):
        self.change_state()
        QTimer.singleShot(1000, self.testing)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if self.line_width > 0:
            painter.setPen(QPen(QColor("#535353"), self.line_width))
        else:
            painter.setPen(Qt.NoPen)
        if not self.state:
            painter.setBrush(self.state1_color)
        else:
            painter.setBrush(self.state2_color)

        painter.drawEllipse(event.rect().center(), self.radius, self.radius)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication, QHBoxLayout, QPushButton
    app = QApplication([])
    w = QWidget()
    v = QHBoxLayout(w)
    circle = StateWidget()
    v.addWidget(circle)
    b = QPushButton("CHANGE")
    b.clicked.connect(circle.change_state)
    v.addWidget(b)
    w.show()
    app.exec_()
