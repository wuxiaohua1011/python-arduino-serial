from __future__ import print_function, division, absolute_import

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
        serial_file = open_serial_port(baudrate=115200, timeout=1)
    except Exception as e:
        raise e

    # for i in range(10):
    #     try:
    #         write_order(serial_file, Order.HELLO)
    #         receive_order: Order = read_order(serial_file)
    #         print(i, receive_order)
    #         if receive_order in [Order.ALREADY_CONNECTED]:
    #             break
    #         else:
    #             print("trying to connect...")
    #             time.sleep(2.0)
    #     except:
    #         print("trying to connect...")
    #         time.sleep(2.0)

    # print("-----------------")
    # for i in range(10):
    #     write_order(serial_file, Order.STOP)

    #     receive_order: Order = read_order(serial_file)
    #     print(i, receive_order)

    # serial_file = reconnect()

    # # Equivalent to write_i8(serial_file, Order.MOTOR.value)
    # while True:
    #     try:
    #         write_order(serial_file, Order.STOP)
    #         receive_order1: Order = read_order(serial_file)
    #         receive_order2: Order = read_order(serial_file)

    #         # code = read_i16(serial_file)

    #         print(
    #             f"receive_order1: {receive_order1} | receive_order2: {receive_order2} | time: {time.time()} "
    #         )
    #     except Exception as e:
    #         print(e)
