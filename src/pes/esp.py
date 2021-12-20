import time
import sys
import serial

from PyQt5.QtCore import (
    QObject,
)
from PyQt5.QtSerialPort import (
    QSerialPort,
    QSerialPortInfo,
)


class ESP(QObject):
    def __init__(self, port="/dev/ttyUSB0", parent=None):
        super().__init__(parent)
        self.port = port
        self.baud_rate = 115200
        self.serial = QSerialPort()
        self.serial.setBaudRate(self.baud_rate)
        self.serial.setPortName(self.port)
        print(self.serial.open(QSerialPort.ReadWrite))
        self.execute("jeje")

    def _enter_raw_mode(self):
        # self.serial.write(b"\r\x02")
        # self.serial.write(b"\r\x03\x03\x03")
        self.serial.writeData(b"\r\x02")
        self.serial.writeData(b"\r\x03\x03\x03")

        print(self.serial.readAll())
        self.serial.write(b"\r\x01")

        print(self.serial.readAll())

    def _exit_raw_mode(self):
        self.serial.write(b"\x02")

    def execute(self, command: str):
        result = ""
        self._enter_raw_mode()
        self._exit_raw_mode()
        return result


def enter_raw_mode(ser):
    ser.write(b"\r\x02")
    ser.write(b"\r\x03\x03\x03")  # 3 times
    # Flush
    n = ser.in_waiting
    while n > 0:
        ser.read(n)
        n = ser.in_waiting
    ser.write(b"\r\x01")

    data = ser.read_until(b"raw REPL; CTRL-B to exit\r\n>")
    # print(f" [debug]{data.decode()}")

    # ser.write(b"\x04")
    # data = ser.read_until(b"soft reboot\r\n")
    # print(f" [debug]{data.decode()}")
    # Flush
    n = ser.in_waiting
    while n > 0:
        ser.read(n)
        n = ser.in_waiting


def exit_raw_mode(ser):
    ser.write(b"\x02")  # Send CTRL-B to get out of raw mode.


def execute(command, ser):
    print("EXECUTING: ", command)
    enter_raw_mode(ser)
    result = ""
    for cmd in command:
        cmd_bytes = cmd.encode("utf-8")
        ser.write(cmd_bytes)
        ser.write(b"\x04")
        response = ser.read_until(b"\x04>")
        result += response.decode()
        print(f"     RESPONSE={response.decode()}")
    exit_raw_mode(ser)
    return result


def ls(ser):
    command = [
        "import os",
        "print(os.listdir())"
    ]
    files = execute(command, ser)
    list_files = list(map(str.strip, files[files.index("[") + 1:files.index("]")].replace("'", "").split(",")))
    return list_files


if __name__ == "__main__":
    arg = sys.argv[1]
    command = arg.split(";")
    try:
        serial_port = serial.Serial(port="/dev/ttyUSB0", baudrate=115200)
        execute(command, serial_port)
    finally:
        serial_port.close()
