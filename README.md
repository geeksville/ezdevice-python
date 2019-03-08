# EZDevice-python

This project is in alpha test - you probably don't want this yet.

# Installation

You can install this package with the [pip utility](https://pypi.org/project/ezdevice/) (this project requires python 3):

pip install ezdevice-python

# Programming new devices

This tool _should_ automate the process of installing a ezdevice binary onto a new device. You run it as follows

ezdevice --install BOARDTYPE

Where boardtype is a single letter:

- L for the TTGO T5 with a 2.13" eink screen
- K for the TTGO T5 with a 2.9" two color eink screen
- M for the TTGO T5s with a two color eink screen
- R for the TTGO T4
- O for the TTGO with a 18650 battery and OLED screen (I'm not sure if this has a model number)
- G for the TTGO GROW plant sensor

Support for other device types will be released soon.

Example session:

```
mymachine:~$ ezdevice --install L
Downloading firmware for board type L from https://joyfirmware.s3.amazonaws.com/firmware-L.bin
esptool.py v2.6
Found 1 serial ports
Serial port /dev/ttyUSB0
Connecting......
Detecting chip type... ESP32
Chip is ESP32D0WDQ6 (revision 1)
Features: WiFi, BT, Dual Core, 240MHz, VRef calibration in efuse, Coding Scheme None
MAC: XXX
Uploading stub...
Running stub...
Stub running...
Changing baud rate to 921600
Changed.
Configuring flash size...
Auto-detected Flash size: 4MB
Compressed 926960 bytes to 509378...
Wrote 926960 bytes (509378 compressed) at 0x00010000 in 8.3 seconds (effective 898.4 kbit/s)...
Hash of data verified.

Leaving...
Hard resetting via RTS pin...
esptool.py v2.6
Found 1 serial ports
Serial port /dev/ttyUSB0
Connecting........_
Detecting chip type... ESP32
Chip is ESP32D0WDQ6 (revision 1)
Features: WiFi, BT, Dual Core, 240MHz, VRef calibration in efuse, Coding Scheme None
MAC: XXX
Uploading stub...
Running stub...
Stub running...
Changing baud rate to 921600
Changed.
Erasing region (may be slow depending on size)...
Erase completed successfully in 3.4 seconds.
Hard resetting via RTS pin...
No preconfigured wifi settings found
  Please use your phone to connect to the wifi from your new device and tell it your wifi settings
  The SSID will be EZdevice-XXXX
```

# Author

Kevin Hester, kevinh@geeksville.com

# License

FIXME add MIT license

# Contributing

The root repository for this project is located at https://github.com/geeksville/ezdevice-python. Issues and pull requests are gratefully accepted.
