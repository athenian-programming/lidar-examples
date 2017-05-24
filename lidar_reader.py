#!/usr/bin/env python3

import argparse

from serial_reader import DEFAULT_BAUD
from serial_reader import SerialReader
from utils import sleep, setup_logging


def print_data(str, userdata):
    tup = eval(str)
    cms = int(tup[0])
    inches = float(tup[1])
    print("{0} cms - {1} inches".format(cms, inches))


if __name__ == "__main__":
    # Set up CLI
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--serial", default="ttyACM0", type=str,
                        help="Arduino serial port [ttyACM0] (OSX is cu.usbmodemXXXX, Windows is COMX)")
    parser.add_argument("-b", "--baud", default=DEFAULT_BAUD, type=int,
                        help="Arduino serial port baud rate [{0}]".format(DEFAULT_BAUD))
    args = vars(parser.parse_args())

    # Setup logging
    setup_logging()

    # Run SerialReader
    reader = SerialReader(print_data, port=args["serial"], baudrate=args["baud"])
    reader.start()

    # Wait for ctrl-C
    try:
        sleep()
    except KeyboardInterrupt:
        pass
    finally:
        # Stop threads
        reader.stop()

    print("Exiting...")
