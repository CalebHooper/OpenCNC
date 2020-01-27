import os
import ezdxf
from glob import glob
from subprocess import check_output, CalledProcessError


def getUsbDevices():
    sdb_devices = map(os.path.realpath, glob('/sys/block/sd*'))
    usb_devices = (dev for dev in sdb_devices
        if 'usb' in dev.split('/')[5])
    return dict((os.path.basename(dev), dev) for dev in usb_devices)

def getMountPoints(devices=None):
    devices = devices or getUsbDevices()  # if devices are None: get_usb_devices
    output = check_output(['mount']).splitlines()
    output = [tmp.decode('UTF-8') for tmp in output]

    def is_usb(path):
        return any(dev in path for dev in devices)
    usb_info = (line for line in output if is_usb(line.split()[0]))
    return [(info.split()[0], info.split()[2]) for info in usb_info]


def loadDXF():

    dxf = ""

    # No USB Device Inserted
    if len(getMountPoints()) <= 0:
        return False

    for File in os.listdir(getMountPoints()[0][1]):
        if File.endswith(".DXF"):
            dxf = getMountPoints()[0][1] + "/" + File

    # No DXF File Found On USB Device
    if dxf == "":
        return False

    return dxf
