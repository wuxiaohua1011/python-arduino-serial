from __future__ import print_function, division, absolute_import
import serial
import time

from robust_serial import (
    write_order,
    Order,
    write_i8,
    write_i16,
    read_i8,
    read_order,
    read_i16,
)
from robust_serial.utils import open_serial_port


def reconnect():
    try:
        serial_file = open_serial_port(baudrate=115200, timeout=None)
    except Exception as e:
        raise e

    is_connected = False
    # Initialize communication with Arduino
    while not is_connected:
        print("Waiting for arduino...")
        write_order(serial_file, Order.HELLO)
        receive_order: Order = read_order(serial_file)

        # bytes_array = bytearray(serial_file.read(1))
        print(receive_order)

        # if not bytes_array:
        #     time.sleep(2)
        #     continue
        receive_order: Order = read_order(serial_file)
        print(receive_order)
        if receive_order in [Order.HELLO, Order.ALREADY_CONNECTED, Order.RECEIVED]:
            is_connected = True

        receive_order: Order = read_order(serial_file)
        print(receive_order)
    return serial_file


if __name__ == "__main__":

    try:
        serial_file = serial.Serial(
            port="/dev/cu.usbmodem11401", baudrate=115200, timeout=1, writeTimeout=1
        )
    except Exception as e:
        raise e

    # clear buffer
    # for i in range(5):
    #     try:
    #         received_order = read_order(serial_file)
    #     except:
    #         pass
    # print("buffer cleaned")

    # ensure connection is good
    for i in range(10):
        write_order(serial_file, Order.HELLO)
        try:
            received_order = read_order(serial_file)
            if received_order in [Order.HELLO, Order.ALREADY_CONNECTED]:
                print("connection success")
                received_order = read_order(serial_file)
                if received_order in [Order.RECEIVED]:
                    print("Receipt confirmed, ready for data")
                    break
            print("trying again")
        except Exception as e:
            print(e)

    cmd_sent_but_not_confirmed = 0
    while True:
        cmd_sent_but_not_confirmed += 1
        write_order(serial_file, Order.STOP)
        received_order = read_order(serial_file)
        if received_order in [Order.RECEIVED]:
            cmd_sent_but_not_confirmed -= 1
        print(received_order, cmd_sent_but_not_confirmed, time.time())
