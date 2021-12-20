import logging

from PyQt5.QtWidgets import (
    QMainWindow,
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import (
    Qt,
    pyqtSignal,
)

from pes.main_panel import MainPanel
from pes.statusbar import StatusBar

logger = logging.getLogger(__name__)


class IDE(QMainWindow):
    goingDown = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PES")
        self.main_panel = MainPanel()
        self.setCentralWidget(self.main_panel)
        self.status_bar = StatusBar(self, parent=self.statusBar())
        self.statusBar().addWidget(self.status_bar, 1)
        self.statusBar().setSizeGripEnabled(False)
        self.statusBar().show()

        # FEO
        # self.main_panel.editor_widget.editor.cursorPositionChanged.connect(self.status_bar.update_line_col)

    def closeEvent(self, event):
        super().closeEvent(event)
        self.goingDown.emit()
