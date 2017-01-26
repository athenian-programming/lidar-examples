#!/usr/bin/env python3

import argparse
import logging
import sys
import time

from common_constants import LOGGING_ARGS
from common_utils import is_windows
from pyfirmata import Arduino
from pyfirmata import INPUT

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--serial", default="ttyACM0", type=str,
                        help="Arduino serial port [ttyACM0] (OSX is cu.usbmodemXXXX)")
    args = vars(parser.parse_args())

    # Setup logging
    logging.basicConfig(**LOGGING_ARGS)

    # Setup firmata client
    port = "/dev/" if not is_windows() else "" + args["serial"]

    try:
        board = Arduino(port)
        logging.info("Connected to Arduino at: {0}".format(port))
    except OSError as e:
        logging.error("Failed to connect to Arduino at {0} - [{1}]".format(port, e))
        sys.exit(0)

    pin2 = board.get_pin("d:2:o")
    pin3 = board.get_pin("d:3:p")

    pin2.write(0)
    pin3.mode = INPUT

    while True:
        print(pin3.read())
        time.sleep(1)
