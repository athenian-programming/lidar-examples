#!/usr/bin/env python3

import argparse
import logging
import sys
import time

import serial

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--serial", default="ttyACM0", type=str,
                        help="Arduino serial port [ttyACM0] (OSX is cu.usbmodemXXXX)")
    args = vars(parser.parse_args())

    logging.basicConfig(stream=sys.stderr, level=logging.INFO,
                        format="%(asctime)s %(name)-10s %(funcName)-10s():%(lineno)i: %(levelname)-6s %(message)s")

    port = "/dev/" + args["serial"]

    try:
        ser = serial.Serial(port=port, baudrate=115200)
    except serial.serialutil.SerialException as e:
        print(e)
        sys.exit(0)

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
