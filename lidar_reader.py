#!/usr/bin/env python3

import argparse
import logging

from common_constants import LOGGING_ARGS
from common_utils import sleep
from serial_reader import DEFAULT_BAUD
from serial_reader import SerialReader


def print_data(str):
    tup = eval(str)
    cms = int(tup[0])
    inches = float(tup[1])
    print(str(cms) + " : " + str(inches))


if __name__ == "__main__":
    # Set up CLI
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--serial", default="ttyACM0", type=str,
                        help="Arduino serial port [ttyACM0] (OSX is cu.usbmodemXXXX, Windows is COMX)")
    parser.add_argument("-b", "--baud", default=DEFAULT_BAUD, type=int,
                        help="Arduino serial port baud rate [{0}]".format(DEFAULT_BAUD))
    args = vars(parser.parse_args())

    # Setup logging
    logging.basicConfig(**LOGGING_ARGS)

    # Run SerialReader
    reader = SerialReader()
    reader.start(print_data, args["serial"], baudrate=args["baud"])

    # Wait for ctrl-C
    try:
        sleep()
    except KeyboardInterrupt:
        pass
    finally:
        # Stop threads
        reader.stop()

    print("Exiting...")
