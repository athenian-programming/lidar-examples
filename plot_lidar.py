import argparse
import datetime
import logging
import time

import plotly.graph_objs as go
import plotly.plotly as py
import plotly.tools as tls
from common_constants import LOGGING_ARGS
from common_utils import is_windows

from lidar_reader import LidarReader

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--serial", default="ttyACM0", type=str,
                        help="Arduino serial port [ttyACM0] (OSX is cu.usbmodemXXXX, Windows is COMX)")
    args = vars(parser.parse_args())

    # Setup logging
    logging.basicConfig(**LOGGING_ARGS)

    lidar = LidarReader()

    # Setup Plot.ly
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

    # Open stream
    stream = py.Stream(stream_id)
    stream.open()
    logging.info("Opened plot.ly stream")
    time.sleep(5)


    def plot_data(tup):
        cms = int(tup[0])
        inches = float(tup[1])
        x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        stream.write(dict(x=x, y=cms))


    # Start consumer thread
    lidar.start_consumer(plot_data)

    # Start producer thread
    port = ("" if is_windows() else "/dev/") + args["serial"]
    lidar.start_producer(port)

    # Wait for ctrl-C
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        pass
    finally:
        # Stop threads
        lidar.stop()

        # Shutdown Plot.ly
        stream.close()

    print("Exiting...")
