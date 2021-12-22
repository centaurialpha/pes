import os
import builtins
import keyword

from PyQt5.QtWidgets import (
    QLabel,
    QTabWidget,
    QMessageBox,
    QWidget,
    QVBoxLayout,
)
from PyQt5.QtGui import (
    QColor,
)
from PyQt5.Qsci import (
    QsciScintilla,
    QsciLexerPython,
)
from PyQt5.QtCore import (
    pyqtSlot,
)

from pes.theme import DarkTheme


class PythonLexer(QsciLexerPython):
    BACKGROUND_COLOR = "#282a36"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keywords_list = keyword.kwlist.copy()
        for k in ("False", "None", "True"):
            self.keywords_list.remove(k)

        self.builtins = list(builtins.__dict__.keys()) + ["self", "cls"]
        for k in ("False", "None", "True"):
            self.builtins.append(k)

    def keywords(self, keyset):
        if keyset == 1:
            keywords = self.keywords_list
        elif keyset == 2:
            keywords = self.builtins
        else:
            return None
        return " ".join(keywords)


class BaseEditor(QsciScintilla):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lexer = PythonLexer()
        self.setLexer(self.lexer)

    def apply_theme(self, theme=DarkTheme):
        theme.apply(self.lexer)


class REPL(BaseEditor):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMargins(0)
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)

        self.apply_theme()

    def keyPressEvent(self, event):
        print(event.text())
        super().keyPressEvent(event)


class Editor(BaseEditor):
    def __init__(self, path=None, parent=None):
        super().__init__(parent)
        self.path = path
        self.setModified(False)
        self.configure()

        self.linesChanged.connect(self._update_sidebar)

    def _update_sidebar(self):
        self.setMarginWidth(0, str(self.lines()) + "0")

    def configure(self):
        self.setAutoIndent(True)
        self.setIndentationWidth(4)
        self.setTabWidth(4)

        self.setMargins(1)
        self.setMarginType(0, QsciScintilla.NumberMargin)
        self.setMarginsBackgroundColor(QColor("#282a36"))
        self.setMarginsForegroundColor(QColor("#aaaaaa"))
        self.setCaretWidth(3)
        self.setCaretForegroundColor(QColor("#ffffff"))
        # Brace matching
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.SendScintilla(QsciScintilla.SCI_INDICSETSTYLE, 4, QsciScintilla.INDIC_STRAIGHTBOX)
        self.SendScintilla(QsciScintilla.SCI_INDICSETSTYLE, 5, QsciScintilla.INDIC_STRAIGHTBOX)
        self.setMatchedBraceIndicator(4)
        self.setUnmatchedBraceIndicator(5)
        for ind in (4, 5):
            self.SendScintilla(QsciScintilla.SCI_INDICSETALPHA, ind, 50)
            self.SendScintilla(QsciScintilla.SCI_INDICSETOUTLINEALPHA, ind, 100)
        self.SendScintilla(QsciScintilla.SCI_INDICSETFORE, 4, QColor("#50fa7b"))
        self.SendScintilla(QsciScintilla.SCI_INDICSETFORE, 5, QColor("#ff5555"))

        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)

        # Folding
        # TODO folding
        self.apply_theme()
        self._update_sidebar()

        self._test()

    def _test(self):
        if self.path is None:
            code = (
                "import time\nfrom machine import Pin\n\nled = Pin(2, Pin.OUT)\n"
                "while True:\n    led.off()\n    time.sleep_ms(500)\n"
                "    led.on()\n    time.sleep_ms(500)"
            )
            self.setText(code)

    def apply_theme(self, theme=DarkTheme):
        theme.apply(self.lexer)

    @property
    def display_text(self) -> str:
        text = "untitled"
        if self.path is not None:
            text = os.path.basename(self.path)
        return text

    @property
    def modified(self) -> bool:
        return self.isModified()


class EditorTab(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setTabsClosable(True)
        self.setMovable(True)

        # Corner widget
        self.line_col_text = "Lin: {}, Col: {}"
        self.line_col_label = QLabel(self.line_col_text)
        self.setCornerWidget(self.line_col_label)
        self.tabCloseRequested.connect(self.removeTab)

    @property
    def current_editor(self) -> Editor:
        return self.currentWidget()

    @property
    def current_index(self) -> int:
        return self.currentIndex()

    @property
    def display_text(self) -> str:
        return self.current_editor.display_text

    @property
    def current_text(self) -> str:
        return self.tabText(self.current_index)

    @current_text.setter
    def current_text(self, text):
        self.setTabText(self.current_index, text)

    def removeTab(self, index):
        if self.current_editor.modified:
            ret = QMessageBox.question(
                self,
                "jeje",
                f"jejejeje {self.current_editor.display_text}",
                QMessageBox.Save | QMessageBox.Cancel
            )
            print(ret)
            print("SI")
        else:
            print("NO")
        super().removeTab(index)

    def update_line_col(self, line: int, col: int):
        self.line_col_label.setText(self.line_col_text.format(line + 1, col))


class EditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        vbox = QVBoxLayout(self)
        self.editor_tab = EditorTab()
        vbox.addWidget(self.editor_tab)

    def add_editor(self, path):
        ed = Editor(path)
        # FIXME: feo feo
        # hacer función que lea en binario y decodifique
        if path is not None:
            with open(path) as fp:
                text = fp.read()
            ed.setText(text)
        # Connect signals
        ed.cursorPositionChanged.connect(self.editor_tab.update_line_col)
        ed.modificationChanged.connect(self.on_modification_changed)

        index = self.editor_tab.addTab(ed, ed.display_text)
        self.editor_tab.setTabToolTip(index, ed.path)
        self.editor_tab.setCurrentIndex(index)
        ed.setFocus()

    @pyqtSlot(bool)
    def on_modification_changed(self, modified):
        title = self.editor_tab.current_text
        if modified:
            title = f"{title} •"
        else:
            title = self.editor_tab.display_text
        self.editor_tab.current_text = title
