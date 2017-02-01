#!/usr/bin/env python3

import argparse
import logging
import sys
import time
import traceback
from threading import Event
from threading import Lock
from threading import Thread

import serial
from common_constants import LOGGING_ARGS
from common_utils import is_windows

DEFAULT_BAUD = 115200


class LidarReader(object):
    def __init__(self):
        self.lock = Lock()
        self.event = Event()
        self.stopped = False
        self.data = None

    # Read data from serial port and pass it along to the consumer
    # If the consumer runs slower than the producer, then values will be dropped
    def produce_data(self, port, baudrate):
        ser = None
        try:
            # Open serial port
            ser = serial.Serial(port=port, baudrate=baudrate)

            while not self.stopped:
                try:
                    # Read data from serial port.  Ignore the trailing two chars with [:-2]
                    bytes = ser.readline()[:-2]

                    # Update data with mutex
                    with self.lock:
                        self.data = bytes.decode("utf-8")

                    # Notify consumer data is ready
                    self.event.set()

                except BaseException as e:
                    print(e)
                    time.sleep(1)

        except serial.serialutil.SerialException as e:
            traceback.print_exc()
            sys.exit(0)

        finally:
            if ser is not None:
                ser.close()

    # Consume data without doing a busy wait
    # If the consumer runs faster than the producer, it will wait on self.event
    def consume_data(self, func):
        while not self.stopped:
            try:
                # Wait for data
                self.event.wait()

                # Reset event to trigger wait on net iteration
                self.event.clear()

                # Read data with mutex
                with self.lock:
                    tuple = eval(self.data)

                # Call func with data
                func(tuple)

            except BaseException as e:
                traceback.print_exc()
                time.sleep(1)

    def start_producer(self, port, baudrate=DEFAULT_BAUD):
        port_path = ("" if is_windows() else "/dev/") + port
        Thread(target=self.produce_data, args=(port_path, baudrate)).start()

    def start_consumer(self, func):
        Thread(target=self.consume_data, args=(func,)).start()

    def stop(self):
        self.stopped = True


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

    # Create LidarReader
    lidar = LidarReader()


    def print_data(tuple):
        cms = int(tuple[0])
        inches = float(tuple[1])
        print(str(cms) + " : " + str(inches))


    # Start consumer thread
    lidar.start_consumer(print_data)

    # Start producer thread
    lidar.start_producer(args["serial"], baudrate=args["baud"])

    # Wait for ctrl-C
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        pass
    finally:
        # Stop threads
        lidar.stop()

    print("Exiting...")
