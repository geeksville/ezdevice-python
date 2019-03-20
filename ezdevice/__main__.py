#!python

import argparse
from .client import EZDeviceClient


def main():
    """Perform command line ezdevice operations"""
    parser = argparse.ArgumentParser()

    # Operations for manufacturing
    parser.add_argument("--install", choices=['R', 'L', 'M', 'O', 'G', 'K', 'Y'],
                        help="Install the ezdevice code onto a new device (you must select the board type letter - see README.md)")
    parser.add_argument("--readee", action="store_true",
                        help="Extract the eeprom contents from the device, so it can be programmed onto other boards")

    # Operations for app developers
    parser.add_argument(
        "--target", help="The device we are controlling given as ID (secretkey will be added later)")
    parser.add_argument(
        "--displayfile", help="display a text,html,png,svg or jpeg file on the display")
    # parser.add_argument("--displayURL", help="display a text,html,png,svg or jpeg from the web on the device")
    parser.add_argument(
        "--release", help="Mark that this device is no longer being used for custom development (i.e. return to joyframe demo app)")

    # Operations for server backend developers
    parser.add_argument("--localserve", help="Talk to a development server",
                        action="store_true")

    args = parser.parse_args()

    client = EZDeviceClient(not args.localserve)

    if args.install:
        client.installFirmware(args.install)
    elif args.readee:
        client.readEEprom()
    elif args.target:
        if args.displayfile:
            client.displayfile(args.target, args.displayfile)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
