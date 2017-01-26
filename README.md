# Lidar Examples

## Installation

Instal pyserial with:
```bash
$ pip install pyserial
```

## Garmin Lidar Lite v3

* The Lidar Lite can be purchased [here](https://www.sparkfun.com/products/14032).

* The specs and wiring diagrams are 
[here](http://static.garmin.com/pumac/LIDAR_Lite_v3_Operation_Manual_and_Technical_Specifications.pdf).

* The Arduino Library is [here](https://github.com/garmin/LIDARLite_v3_Arduino_Library).

## ADAFRUIT VL53L0X TIME OF FLIGHT DISTANCE SENSOR

* The VL53L0X can be purchased [here](https://www.adafruit.com/products/3317).

* The tutorial is [here](https://learn.adafruit.com/adafruit-vl53l0x-micro-lidar-distance-sensor-breakout).


## Plot.ly

Details on setting up plot.ly are 
[here](http://www.athenian-robotics.org/site/plotly/).

### Usage 

```bash
$ lidar_lite_serial.py --port cu.usbmodem1451 
```

### CLI Options

| Option         | Description                                        | Default |
|:---------------|----------------------------------------------------|---------|
| -s, --serial   | Arduino serial port                                | ttyACM0 |
