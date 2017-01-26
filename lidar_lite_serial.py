#!/usr/bin/env python3

import argparse
import logging
import sys
import time

import serial
from common_constants import LOGGING_ARGS
from common_utils import is_windows

if __name__ == "__main__":
    # Set up CLI
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--serial", default="ttyACM0", type=str,
                        help="Arduino serial port [ttyACM0] (OSX is cu.usbmodemXXXX, Windows is COMX)")
    args = vars(parser.parse_args())

    # Setup logging
    logging.basicConfig(**LOGGING_ARGS)

    port = ("" if is_windows() else "/dev/") + args["serial"]

    try:
        ser = serial.Serial(port=port, baudrate=115200)
    except serial.serialutil.SerialException as e:
        print(e)
        sys.exit(0)

    try:
        while True:
            try:
                bytes = ser.readline()[:-2]
                s = bytes.decode("utf-8")
                tup = eval(s)
                cms = int(tup[0])
                inches = float(tup[1])
                print(str(cms) + " : " + str(inches))
            except BaseException as e:
                print(e)
                time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        ser.close()
