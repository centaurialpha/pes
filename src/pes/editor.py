import builtins
import keyword

from PyQt5.QtGui import (
    QFont,
    QColor,
    QFontMetrics,
    QPainter,
)
from PyQt5.Qsci import (
    QsciScintilla,
    QsciLexerPython,
)

from pes.theme import DarkTheme

"""
KEYWORDS defined in QsciPythonLexer

and as assert break class continue def del elif else except exec
finally for from global if import in is lambda None not or pass
print raise return try while with yield
"""


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


class Editor(QsciScintilla):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lexer = PythonLexer()
        self.setLexer(self.lexer)
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
        code = (
            "import time\nfrom machine import Pin\n\nled = Pin(2, Pin.OUT)\n"
            "while True:\n    led.off()\n    time.sleep_ms(500)\n"
            "    led.on()\n    time.sleep_ms(500)"
        )
        self.setText(code)

    def apply_theme(self, theme=DarkTheme):
        theme.apply(self.lexer)
