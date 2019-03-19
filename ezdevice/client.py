

import sys
import urllib.request
import esptool
import os.path

# FIXME - clean these files up - store in a temp directory
bucketname = "joyfirmware"
eefile = "eeprom.bin"
nvsfile = "nvs.bin"


def runEsptool(args):
    """Run esptool with appropriate connection/baudrate options"""
    stdopts = ["-b", "921600"]
    esptool.main(stdopts + args)


class EZDeviceClient:
    """Client nub for talking to EZdevice servers"""

    def installFirmware(self, boardType):
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

    def readEEprom(self):
        """Pull the eeprom contents onto the local filesystem"""
        runEsptool(["read_flash", "0x290000", "0x1000", eefile])
        runEsptool(["read_flash", "0x9000", "0x5000", nvsfile])

    def displayfile(self, target, filepath):
        """Show the indicated file on the display"""
        # FIXME, set the app owner for the device to something other than joyframe
        print("not yet implemented")
