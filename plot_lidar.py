import argparse
import datetime
import logging
import sys
import time

import plotly.graph_objs as go
import plotly.plotly as py
import plotly.tools as tls
import serial
from common_constants import LOGGING_ARGS
from common_utils import is_windows

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--serial", default="ttyACM0", type=str,
                        help="Arduino serial port [ttyACM0] (OSX is cu.usbmodemXXXX)")
    args = vars(parser.parse_args())

    # Setup logging
    logging.basicConfig(**LOGGING_ARGS)

    port = "/dev/" if not is_windows() else "" + args["serial"]

    stream_ids = tls.get_credentials_file()['stream_ids']
    stream_id = stream_ids[0]

    # Declare graph
    graph = go.Scatter(x=[],
                       y=[],
                       mode='lines+markers',
                       stream=dict(token=stream_id, maxpoints=80))
    data = go.Data([graph])
    layout = go.Layout(title='Distance (cms)')
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='plot-positions')

    # Write data
    stream = py.Stream(stream_id)
    stream.open()

    logging.info("Opening plot.ly tab")
    time.sleep(5)

    try:
        serial = serial.Serial(port=port, baudrate=115200)
    except serial.serialutil.SerialException as e:
        print(e)
        sys.exit(0)

    try:
        while True:
            try:
                bytes = serial.readline()[:-2]
                tup = eval(bytes.decode("utf-8"))
                cms = int(tup[0])
                inches = float(tup[1])
                x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                stream.write(dict(x=x, y=cms))
            except BaseException as e:
                print(e)
                time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        stream.close()
        serial.close()
