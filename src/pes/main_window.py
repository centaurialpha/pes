import logging

from PyQt5.QtWidgets import (
    QMainWindow,
    QFileDialog,
)
from PyQt5.QtCore import (
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

        self.load_menu()

    def _changed(self, d):
        print(d)

    def _on_check_ports(self, ports):
        self.statusBar().showMessage("Searching...", 1000)
        self.status_bar.device_status.update_text("Connected")
        self.status_bar.device_status.state_widget.change_state()

    def load_menu(self):
        # FIXME: FEO FEO
        # mover esto a otro lugar
        # los menu,actions deben poder crearse de otra manera, para extensión
        menubar = self.menuBar()
        menu_file = menubar.addMenu("&File")
        new_file_act = menu_file.addAction("New File")
        new_file_act.triggered.connect(self.add_new_tab)
        new_file_act.setShortcut("Ctrl+N")
        open_file_act = menu_file.addAction("Open file")
        open_file_act.triggered.connect(self.open_file)
        open_file_act.setShortcut("Ctrl+O")
        close_file_act = menu_file.addAction("Close File")
        close_file_act.triggered.connect(self.close_tab)
        close_file_act.setShortcut("Ctrl+W")

    def add_new_tab(self):
        self.main_panel.new_tab(path=None)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open File")
        if filename:
            self.main_panel.new_tab(path=filename)

    def close_tab(self):
        self.main_panel.close_tab()

    def closeEvent(self, event):
        super().closeEvent(event)
        self.goingDown.emit()
