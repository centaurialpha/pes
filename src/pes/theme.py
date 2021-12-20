from dataclasses import dataclass

from PyQt5.QtGui import QColor, QFont
from PyQt5.QtGui import QPalette


DARK = {
    'Window': '#171a21',
    'WindowText': '#ffffff',
    'WindowTextDisabled': '#7f7f7f',
    'Base': '#282a36',
    'AlternateBase': '#1c1e26',
    'ToolTipBase': '#2e3139',
    'ToolTipText': '#ffffff',
    'Text': '#dddddd',
    'TextDisabled': '#505050',
    'Dark': '#232323',
    'Shadow': '#323228',
    'Button': '#191a1f',
    'ButtonText': '#ffffff',
    'ButtonTextDisabled': '#7f7f7f',
    'BrightText': '#ec7875',
    'Link': '#2a82da',
    'Highlight': '#42539e',
    'Mid': '#404040',
    'Midlight': '#ff0000',
    'HighlightDisabled': '#505050',
    'HighlightedText': '#f1f1f1',
    'HighlightedTextDisabled': '#7f7f7f'
}


LIGHT = {
    'Highlight': '#7742539e',
    'BrightText': '#ec7875',
    'Dark': '#dddddd'
}

EDITOR_DARK = {
    # Editor
    'background': '#282a36',
    'foreground': '#f8f8f2',
    'sidebar_background': '#282a36',
    'sidebar_foreground': '#6272a4',
    'current_line': '#383b4c',
    # Hihglighter
    'keyword': '#7ce4fb',
    'number': '#bd93f9',
    'string': '#f1fa8c',
    'comment': '#6272a4',
    'operator': '#ffffff',
    'variable': '#ffb86c',
}

EDITOR_LIGHT = {
    'background': '#ffffff',
    'foreground': '#000000',
    'sidebar_background': '#ffffff',
    'sidebar_foreground': '#000000',
    'current_line': '#eeeeee',
    'keyword': '#808000',
    'number': '#000080',
    'string': '#008000',
    'comment': '#008000',
    'operator': '#000000',
    'variable': '#800000',
}


@dataclass
class Style:
    color: str = "#ffffff"
    paper: str = "#282a36"
    bold: bool = False
    italic: bool = False

    @property
    def font(self):
        qfont = QFont("Cascadia Mono", 14)
        qfont.setBold(self.bold)
        qfont.setItalic(self.italic)
        return qfont


class EditorThemeBase:

    @classmethod
    def apply(cls, lexer):
        lexer.setFont(Style().font)

        for name, style in cls.__dict__.items():
            if not isinstance(style, Style):
                continue
            style_num = getattr(lexer, name)
            if not isinstance(style_num, int):
                continue
            lexer.setColor(QColor(style.color), style_num)
            lexer.setPaper(QColor(style.paper), style_num)
            lexer.setFont(style.font, style_num)


class DarkTheme(EditorThemeBase):
    Keyword = Style("#ff79c6", bold=True)
    Comment = Style("#6272a4", bold=True)
    Number = Style("#bd93f9")
    DoubleQuotedString = Style("#f1fa8c")
    SingleQuotedString = Style("#f1fa8c")
    TripleSingleQuotedString = Style("#50fa7b")
    TripleDoubleQuotedString = Style("#50fa7b")
    FunctionMethodName = Style("#50fa7b")
    Operator = Style()
    Identifier = Style()
    CommentBlock = Style()
    UnclosedString = Style("red")
    HighlightedIdentifier = Style("#8be9fd")
    ClassName = Style("#ffb86c")
    Decorator = Style("#99ff99")


class LightTheme(EditorThemeBase):
    pass


def apply_theme(app):
    theme = DARK
    # if SETTINGS.dark_mode:
    #     theme = DARK
    # else:
    #     theme = LIGHT
    #     app.setPalette(app.style().standardPalette())
    palette = QPalette()
    for role_name, color in theme.items():
        if role_name.endswith('Disabled'):
            role_name = role_name.split('Disabled')[0]
            color_group = QPalette.Disabled
        else:
            color_group = QPalette.All
        if not isinstance(color, QColor):
            qcolor = QColor(color)
        else:
            qcolor = color
        color_role = getattr(palette, role_name)
        palette.setBrush(color_group, color_role, qcolor)
    app.setPalette(palette)
