from dataclasses import dataclass

from PyQt5.QtWidgets import (
    QWidget,
    QFrame,
    QDialog,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QToolButton,
    QMainWindow,
    QComboBox,
    QDialogButtonBox,
    qApp,
)
from PyQt5.QtCore import (
    Qt,
    pyqtSignal,
    pyqtSlot,
    QPoint,
)
from PyQt5.QtSerialPort import QSerialPortInfo

from pes.state_widget import StateWidget


@dataclass
class Port:
    name: str
    location: str
    vid: str
    pid: str


class PortListWidget(QDialog):
    connected = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ports = []
        self.setModal(True)
        vbox = QVBoxLayout(self)
        self.combo_box_ports = QComboBox()
        vbox.addWidget(self.combo_box_ports)
        self.port_info_label = QLabel("")
        vbox.addWidget(self.port_info_label)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.rejected.connect(self.reject)
        button_box.accepted.connect(self.accept)
        self.combo_box_ports.currentIndexChanged.connect(self._on_combo_box_changed)

        vbox.addWidget(button_box)

    @pyqtSlot(int)
    def _on_combo_box_changed(self, index):
        port = self.ports[index]
        self.update_info(port)

    def accept(self):
        self.connected.emit()

    def showEvent(self, event):
        super().showEvent(event)
        self.ports.clear()
        available_ports = QSerialPortInfo.availablePorts()
        for port in available_ports:
            port_obj = Port(
                name=port.portName(),
                location=port.systemLocation(),
                vid=port.vendorIdentifier(),
                pid=port.productIdentifier()
            )
            self.ports.append(port_obj)

        for port in self.ports:
            self.combo_box_ports.addItem(port.location)
        self.combo_box_ports.setCurrentIndex(0)

    def update_info(self, port):
        port_info_text = (
            f"<b>Port:</b> {port.name}<br>"
            f"<b>Location:</b> {port.location}<br>"
            f"<b>VID:</b> {port.vid}<br>"
            f"<b>PID:</b> {port.pid}<br>"
        )
        self.port_info_label.setText(port_info_text)


class DeviceStatusWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        hbox = QHBoxLayout(self)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)
        self.state_widget = StateWidget()
        self.state_label = QLabel("Not connected")
        hbox.addWidget(self.state_widget)
        hbox.addWidget(self.state_label)

        self.info_widget = PortListWidget(self)

    def update_text(self, text):
        self.state_label.setText(text)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.info_widget.exec_()


class StatusBar(QFrame):
    def __init__(self, main_window: QMainWindow, parent=None):
        super().__init__(parent)
        self._main_window = main_window

        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        left_widget = QFrame(parent)
        mid_widget = QFrame(parent)
        right_widget = QFrame(parent)

        left_layout = QHBoxLayout(left_widget)
        left_widget.setLayout(left_layout)
        left_layout.setContentsMargins(0, 0, 0, 0)
        mid_layout = QHBoxLayout(mid_widget)
        mid_widget.setLayout(mid_layout)
        mid_layout.setContentsMargins(0, 0, 0, 0)
        right_layout = QHBoxLayout(right_widget)
        right_widget.setLayout(right_layout)
        right_layout.setContentsMargins(0, 0, 0, 0)

        # Left Widgets
        self.device_status = DeviceStatusWidget()
        left_layout.addWidget(self.device_status)

        # Mid Widgets
        settings_btn = QToolButton()
        settings_btn = QToolButton()
        settings_btn.setAutoRaise(True)
        settings_btn.setFocusPolicy(Qt.NoFocus)
        settings_btn.setText('\uf013')

        self.line_col_text = "Lin: {}, Col: {}"
        self.line_col_label = QLabel(self.line_col_text)

        dark_mode_btn = QToolButton()
        dark_mode_btn.setAutoRaise(True)
        dark_mode_btn.setFocusPolicy(Qt.NoFocus)
        dark_mode_btn.setCheckable(True)
        dark_mode_btn.setText('\uf186')
        mid_layout.addWidget(settings_btn)
        mid_layout.addWidget(self.line_col_label)
        mid_layout.addWidget(dark_mode_btn)

        # Right Widgets
        repl_btn = QToolButton()
        repl_btn.setAutoRaise(True)
        repl_btn.setText("\uf101")
        upload_btn = QToolButton()
        upload_btn.setAutoRaise(True)
        upload_btn.setText("\uf574")
        run_btn = QToolButton()
        run_btn.setAutoRaise(True)
        run_btn.setText("\uf04b")
        led_btn = StateWidget()
        led_btn.line_width = 2
        led_btn.clickable = True
        stop_btn = QToolButton()
        stop_btn.setAutoRaise(True)
        stop_btn.setText("\uf04d")

        right_layout.addWidget(led_btn)
        right_layout.addWidget(repl_btn)
        right_layout.addWidget(upload_btn)
        right_layout.addWidget(run_btn)
        right_layout.addWidget(stop_btn)

        layout.addWidget(left_widget, 0, 0, 0, 1, Qt.AlignLeft)
        layout.addWidget(mid_widget, 0, 1, 0, 1, Qt.AlignCenter)
        layout.addWidget(right_widget, 0, 2, 0, 1, Qt.AlignRight)

        layout.setContentsMargins(2, 0, 2, 0)

    def update_line_col(self, line: int, col: int):
        self.line_col_label.setText(self.line_col_text.format(line, col))
        # from pes import esp
        # current_state = self.sender().state
        # self.sender().change_state()
        # command = [
        #     "from machine import Pin",
        #     "l=Pin(2, Pin.OUT)",
        # ]
        # if current_state:
        #     command.append("l.on()")
        # else:
        #     command.append("l.off()")
        # esp.execute(command, self._main_window.serial_port)
