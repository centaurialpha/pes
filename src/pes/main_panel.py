import logging

from PyQt5.QtWidgets import (
    QWidget,
    QSplitter,
    QVBoxLayout,
    QTreeView,
    QFileSystemModel,
    qApp
)
from PyQt5.QtCore import (
    Qt,
)

from pes.editor import (
    REPL,
    EditorWidget,
)
from pes.device import ESP
from pes.control import Control
from pes.filesystem import ROOT_DIR

logger = logging.getLogger(__name__)


class REPLWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.repl = REPL()
        self.ctrl = Control()
        self.ctrl.dataEmited.connect(self.process_data)
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.repl)

    def process_data(self, data):
        data = data.decode()
        self.repl.append(data)


class FileBrowserWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        vbox = QVBoxLayout(self)
        self.filesystemm = QFileSystemModel()
        self.view = QTreeView()
        self.view.setModel(self.filesystemm)
        for i in range(1, 4):
            self.view.hideColumn(i)
        vbox.addWidget(self.view)

    def populate(self):
        self.filesystemm.setRootPath(ROOT_DIR)
        self.view.setRootIndex(self.filesystemm.index(ROOT_DIR))

    def populate2(self):
        import pathlib
        p = pathlib.Path(ROOT_DIR)
        f = p / "oootro.py"
        f.write_text("")


class MainPanel(QSplitter):
    def __init__(self, parent=None, orientation=Qt.Horizontal):
        super().__init__(parent)
        self.esp = ESP()
        self.editor_widget = EditorWidget()
        self.repl_widget = REPLWidget()
        # self.repl_widget.hide()
        self.file_browser_widget = FileBrowserWidget()

        self._vsplitter = QSplitter(orientation=Qt.Vertical)
        self._vsplitter.addWidget(self.editor_widget)
        self._vsplitter.addWidget(self.repl_widget)

        self.addWidget(self.file_browser_widget)
        self.addWidget(self._vsplitter)

    def new_tab(self, path):
        self.editor_widget.add_editor(path)

    def close_tab(self):
        self.editor_widget.editor_tab.removeTab(self.editor_widget.editor_tab.current_index)

    def showEvent(self, event):
        super().showEvent(event)
        geo = qApp.desktop().availableGeometry(self)
        width = geo.width()
        height = geo.height()
        self.setSizes([int(width * 0.20), int(width * 0.80)])
        self._vsplitter.setSizes([int(height * 0.80), int(height * 0.20)])
        # self.editor_widget.editor.setFocus()
