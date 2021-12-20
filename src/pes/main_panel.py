import logging

from PyQt5.QtWidgets import (
    QWidget,
    QSplitter,
    QVBoxLayout,
    QTabWidget,
    QTreeView,
    qApp
)
from PyQt5.QtCore import (
    Qt,
)

from pes.editor import Editor
from pes.device import ESP

logger = logging.getLogger(__name__)


class EditorTab(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setTabsClosable(True)
        self.setMovable(True)


class EditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        vbox = QVBoxLayout(self)
        self.editor = Editor()
        vbox.addWidget(self.editor)
        self.editor.setFocus()


class REPLWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        vbox = QVBoxLayout(self)
        self.editor = Editor()
        vbox.addWidget(self.editor)


class FileBrowserWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        vbox = QVBoxLayout(self)
        self.view = QTreeView()
        vbox.addWidget(self.view)


class MainPanel(QSplitter):
    def __init__(self, parent=None, orientation=Qt.Horizontal):
        super().__init__(parent)
        self.esp = ESP()
        self.editor_widget = EditorWidget()
        self.repl_widget = REPLWidget()
        self.repl_widget.hide()
        self.file_browser_widget = FileBrowserWidget()

        self._vsplitter = QSplitter(orientation=Qt.Vertical)
        self._vsplitter.addWidget(self.editor_widget)
        # self._vsplitter.addWidget(self.repl_widget)

        self.addWidget(self.file_browser_widget)
        self.addWidget(self._vsplitter)

    def showEvent(self, event):
        super().showEvent(event)
        geo = qApp.desktop().availableGeometry(self)
        width = geo.width()
        height = geo.height()
        self.setSizes([int(width * 0.20), int(width * 0.80)])
        self._vsplitter.setSizes([int(height * 0.80), int(height * 0.20)])
        self.editor_widget.editor.setFocus()
