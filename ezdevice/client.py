

import sys
import urllib.request
import esptool
import os.path
import requests
import mimetypes
import json
import logging

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

    def __init__(self, isProd=True):
        """Constructor, !isProd is used only for server development testing"""
        self.urlRoot = 'http://api.ezdevice.net' if isProd else 'http://localhost:3030'

    def installFirmware(self, boardType):
        """Install the latest firmware on a blank device (connect the device to USB before calling this function)"""

        firmwareurl = f"https://{bucketname}.s3.amazonaws.com/firmware-{boardType}.bin"
        logging.debug(
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
            logging.info(
                'PRECONFIGURED WIFI SETTINGS FOUND - they have been installed into the device')
        else:
            logging.info('No preconfigured wifi settings found\n'
                         '  Please use your phone to connect to the wifi from your new device and tell it your wifi settings\n'
                         '  The SSID will be EZdevice-XXXX')

    def readEEprom(self):
        """Use USB to extract device EEprom contents onto the local filesystem (used in factory only)"""
        runEsptool(["read_flash", "0x290000", "0x1000", eefile])
        runEsptool(["read_flash", "0x9000", "0x5000", nvsfile])

    def claim(self, devid):
        """Tell the server that this device is being used for custom development (i.e. turn off default applications)"""

        return self.__patch(devid, {'application': 'ezdevice-python'})

    def release(self, devid):
        """Restore this device to the default application"""

        return self.__patch(devid, {'application': None})

    def displayfile(self, devid, filepath):
        """Show the indicated file on the display"""
        with open(filepath, mode='rb') as fh:
            mydata = fh.read()
            url = "{}/ezdevs/{}/display".format(self.urlRoot, devid)
            logging.debug(f"uploading to {url}")
            response = requests.put(url,
                                    data=mydata,
                                    # auth=('omer', 'b01ad0ce'),
                                    headers={
                                        'content-type':  mimetypes.guess_type(filepath)[0]}
                                    # params={'file': filepath}
                                    )
            if response.status_code != 200:
                raise Exception(f"Error from server {response.text}")

    def __patch(self, devid, patchdict):
        """Patch a device node with JSON data"""

        url = "{}/ezdevs/{}".format(self.urlRoot, devid)
        data = json.dumps(patchdict)
        logging.info(f"patching {url} {data}")
        response = requests.patch(url, data=data, headers={
                                  'content-type': 'application/json'})
        logging.info(f"response {response}")
        if response.status_code != 200:
            raise Exception(f"Error from server {response.text}")
