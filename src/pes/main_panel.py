import logging

from PyQt5.QtWidgets import (
    QWidget,
    QSplitter,
    QVBoxLayout,
    QTabWidget,
    QTreeView,
    QLabel,
    qApp
)
from PyQt5.QtCore import (
    Qt,
    pyqtSlot,
)

from pes.editor import Editor
from pes.device import ESP

logger = logging.getLogger(__name__)


class EditorTab(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setTabsClosable(True)
        self.setMovable(True)

        # Corner widget
        self.line_col_text = "Lin: {}, Col: {}"
        self.line_col_label = QLabel(self.line_col_text)
        self.setCornerWidget(self.line_col_label)

    @property
    def current_editor(self) -> Editor:
        return self.currentWidget()

    @property
    def current_index(self) -> int:
        return self.currentIndex()

    @property
    def current_text(self) -> str:
        return self.tabText(self.current_index)

    @current_text.setter
    def current_text(self, text):
        self.setTabText(self.current_index, text)

    def update_line_col(self, line: int, col: int):
        self.line_col_label.setText(self.line_col_text.format(line + 1, col))


class EditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        vbox = QVBoxLayout(self)
        self.editor_tab = EditorTab()
        vbox.addWidget(self.editor_tab)

    def add_editor(self, title):
        ed = Editor()
        ed.filename = title
        # Connect signals
        ed.cursorPositionChanged.connect(self.editor_tab.update_line_col)
        ed.modificationChanged.connect(self.on_modification_changed)

        index = self.editor_tab.addTab(ed, title)
        self.editor_tab.setCurrentIndex(index)
        ed.setFocus()

    @pyqtSlot(bool)
    def on_modification_changed(self, modified):
        title = self.editor_tab.current_text
        if modified:
            title = f"{title} •"
        else:
            title = self.editor_tab.current_editor.filename
        self.editor_tab.current_text = title


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
        # self.editor_widget.editor.setFocus()
        self.editor_widget.add_editor("hola")
