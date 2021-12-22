import logging

from PyQt5.QtCore import (
    QObject,
    pyqtSignal,
)
from PyQt5.QtSerialPort import QSerialPort

logger = logging.getLogger(__name__)


class Control(QObject):
    CTRL_A = chr(0x01)
    CTRL_B = chr(0x02)
    CTRL_C = chr(0x03)
    CTRL_D = chr(0x04)

    dataEmited = pyqtSignal(bytes)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.serial = QSerialPort()
        self.serial.setBaudRate(115200)
        self.serial.setStopBits(QSerialPort.OneStop)

    def open(self, port):
        self.serial.setPortName(port)
        if not self.serial.open(QSerialPort.ReadWrite):
            logger.error("Could not open port=%s", port)
            return
        self.serial.readyRead.connect(self.read_all)
        self.raw_mode()

    @property
    def port(self):
        return self.serial.portName()

    def raw_mode(self):
        # for _ in range(2):
        #     self.send(Control.CTRL_C)
        # self.send(Control.CTRL_B)
        self.send(Control.CTRL_A)
        # self.send(Control.CTRL_D)
        # for _ in range(2):
        #     self.send(Control.CTRL_C)
        self.read_until("raw REPL; CTRL-B to exit \r\n>")

    def exit_raw_mode(self):
        self.send(Control.CTRL_B)

    def execute(self, commands):
        command_response = bytes()
        for command in commands:
            self.send(command)
            self.send(Control.CTRL_D)
            command_response += self.read_until(Control.CTRL_D)

        return command_response

    def read_all(self):
        data = self.serial.readAll().data()
        self.dataEmited.emit(data)

    def read_until(self, ending):
        if not isinstance(ending, bytes):
            ending = ending.encode()

        data = bytes()

        while self.serial.waitForReadyRead(300):
            if data.endswith(ending):
                break
            data += self.serial.read(1)
        return data

    def send(self, command):
        if not isinstance(command, bytes):
            command = command.encode()
        logger.debug("Sending command=%s to port=%s", command, self.port)
        self.serial.write(command)
