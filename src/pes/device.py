import logging
from dataclasses import dataclass

from PyQt5.QtCore import (
    QObject,
    pyqtSignal,
)
from PyQt5.QtSerialPort import (
    QSerialPort,
    QSerialPortInfo
)

logger = logging.getLogger(__name__)


@dataclass
class Device:
    port: str
    vendor_id: int
    product_id: int
    serial_number: str
    manufacturer: str
    name: str = "ESP8266"


class ESP(QObject):
    VID = 0x1A86
    PID = 0x7523

    connected = pyqtSignal()

    def __init__(self, comm=None, parent=None):
        super().__init__(parent)
        self.comm = comm
        self.device = None

    @property
    def port(self):
        return self.device.port

    def find_device(self):
        logger.info("Looking for ESP...")
        ports = QSerialPortInfo.availablePorts()
        for p in ports:
            vid = p.vendorIdentifier()
            pid = p.productIdentifier()
            if vid == ESP.VID and pid == ESP.PID:
                logger.info("Found %s on %s", vid, p.portName())
                self.device = Device(
                    port="/dev/ttyUSB0",
                    vendor_id=vid,
                    product_id=pid,
                    serial_number=p.serialNumber(),
                    manufacturer=p.manufacturer()
                )
                break

        if self.device is None:
            logger.info("ESP not connected yet")
        else:
            self.connected.emit()


class Comm(QObject):
    CTRL_A = 0x01
    CTRL_B = 0x02
    CTRL_C = 0x03
    CTRL_D = 0x04

    def __init__(self, serial: QSerialPort = None, parent=None):
        super().__init__(parent)
        self.serial = serial

    @classmethod
    def create(cls, port: str):
        ser = QSerialPort()
        ser.setBaudRate(115200)
        ser.setStopBits(QSerialPort.OneStop)
        ser.setPortName(port)
        logger.info("Opening port=%s", port)
        if not ser.open(QSerialPort.ReadWrite):
            logger.warning("Could not open port")
            return cls()
        return cls(ser)

    def send(self, msg):
        self.serial.write(chr(msg).encode("utf-8"))

    def read_until(self, ending, nbytes=1):
        if isinstance(ending, str):
            ending = ending.encode("utf-8")
        elif isinstance(ending, int):
            ending = chr(ending)

        ok = self.serial.waitForReadyRead(3000)
        data = ""
        while ok:
            data += self.serial.readAll().data().decode()
            ok = self.serial.waitForReadyRead(3000)
        return data

    def enter_raw_mode(self):
        self.send(Comm.CTRL_B)
        for _ in range(3):
            self.send(Comm.CTRL_C)
        # self.serial.flush()
        self.send(Comm.CTRL_A)
        self.read_until("raw REPL; CTRL-B to exit \r\n>")

    def exit_raw_mode(self):
        self.send(Comm.CTRL_B)

    def execute(self, commands):
        result = ""
        for command in commands:
            command_bytes = command.encode()
            self.serial.write(command_bytes)
            self.send(Comm.CTRL_D)
            result += self.read_until(Comm.CTRL_D)
        return result


if __name__ == "__main__":
    esp = ESP()
    print(esp.find_device())
