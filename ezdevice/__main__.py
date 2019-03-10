#!python

from configparser import ConfigParser
import sys
import urllib.request
import esptool
import os.path
import argparse

bucketname = "joyfirmware"
eefile = "eeprom.bin"
nvsfile = "nvs.bin"


def runEsptool(args):
    """Run esptool with appropriate connection/baudrate options"""
    stdopts = ["-b", "921600"]
    esptool.main(stdopts + args)


def installFirmware(boardType):
    """Install the latest firmware on a virgin device"""

    firmwareurl = f"https://{bucketname}.s3.amazonaws.com/firmware-J{boardType}.bin"
    print(
        f'Downloading firmware for board type {boardType} from {firmwareurl}')
    localfile = "firmware.bin"
    urllib.request.urlretrieve(firmwareurl, localfile)
    runEsptool(["write_flash", "0x10000", localfile])

    # Don't really need to write the second copy - instead just fill with 0xff
    runEsptool(["erase_region", "0x150000", "0x140000"])

    # If we have a preconfigured files which contain our local wifi settings, install them to make for easy testing

    if os.path.isfile(eefile) and os.path.isfile(nvsfile):
        runEsptool(["write_flash", "0x290000", eefile])
        runEsptool(["write_flash", "0x9000", nvsfile])
        print(
            'PRECONFIGURED WIFI SETTINGS FOUND - they have been installed into the device')
    else:
        print('No preconfigured wifi settings found\n'
              '  Please use your phone to connect to the wifi from your new device and tell it your wifi settings\n'
              '  The SSID will be EZdevice-XXXX')


def readEEprom():
    """Pull the eeprom contents onto the local filesystem"""
    runEsptool(["read_flash", "0x290000", "0x1000", eefile])
    runEsptool(["read_flash", "0x9000", "0x5000", nvsfile])


def displayfile(target, filepath):
    """Show the indicated file on the display"""
    # FIXME, set the app owner for the device to something other than joyframe
    print("not yet implemented")


def main():
    """Perform command line ezdevice operations"""

    parser = argparse.ArgumentParser()

    # Operations for manufacturing
    parser.add_argument("--install", choices=['R', 'L', 'M', 'O', 'G', 'K', 'Y'],
                        help="Install the ezdevice code onto a new device (you must select the board type letter - see README.md)")
    parser.add_argument("--readee", action="store_true",
                        help="Extract the eeprom contents from the device, so it can be programmed onto other boards")

    # Operations for developers
    parser.add_argument(
        "--target", help="The device we are controlling given as ID (secretkey will be added later)")
    parser.add_argument(
        "--displayfile", help="display a text,html,png,svg or jpeg file on the display")
    # parser.add_argument("--displayURL", help="display a text,html,png,svg or jpeg from the web on the device")
    parser.add_argument(
        "--release", help="Mark that this device is no longer being used for custom development (i.e. return to joyframe demo app)")

    args = parser.parse_args()
    if args.install:
        installFirmware(args.install)
    elif args.readee:
        readEEprom()
    elif args.target:
        if args.displayfile:
            displayfile(args.target, args.displayfile)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
