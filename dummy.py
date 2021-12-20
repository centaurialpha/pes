import time
import sys
import serial


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

    ser.write(b"\x04")
    data = ser.read_until(b"soft reboot\r\n")
    # print(f" [debug]{data.decode()}")
    # Flush
    n = ser.in_waiting
    while n > 0:
        ser.read(n)
        print("JJJJJAJAJAJJAJAJA")
        n = ser.in_waitin


def exit_raw_mode(ser):
    ser.write(b"\x02")  # Send CTRL-B to get out of raw mode.


def execute(command, ser):
    enter_raw_mode(ser)
    for cmd in command:
        cmd_bytes = cmd.encode("utf-8")
        ser.write(cmd_bytes)
        ser.write(b"\x04")
        response = ser.read_until(b"\x04>")
        print(f"     RESPONSE={response.decode()}")
    exit_raw_mode(ser)


def ls(ser):
    command = [
        "import os",
        "print(os.listdir())"
    ]
    execute(command, ser)


if __name__ == "__main__":
    arg = sys.argv[1]
    command = arg.split(";")
    try:
        serial_port = serial.Serial(port="/dev/ttyUSB0", baudrate=115200)
        execute(command, serial_port)
    finally:
        serial_port.close()
