from miflora.miflora_poller import MiFloraPoller
from btlewrap.gatttool import GatttoolBackend
import time
import csv
from datetime import datetime
from picamera import PiCamera
from plantcv import plantcv as pcv

FLORA_HOME = '/home/pi/flora'
FLORA_DATA = FLORA_HOME + '/data/'
FLORA_PICS = FLORA_DATA + 'pics/'
FLORA_CSV = FLORA_DATA + 'flora.csv'

MI_TEMPERATURE = "temperature"
MI_LIGHT = "light"
MI_MOISTURE = "moisture"
MI_CONDUCTIVITY = "conductivity"
MI_BATTERY = "battery"

MI_VALUES = {
    MI_TEMPERATURE: {
        'min': 0,
        'max': 40
    },
    MI_LIGHT: {
        'min': 0,
        'max': 10000
    },
    MI_CONDUCTIVITY: {
        'min': 0,
        'max': 600
    }
}

print('plantcv installed, version' + pcv.__version__)
pcv.params.debug = "print"
# TODO - Work in progress...
# obj, mask = pcv.object_composition(img=img, contours=roi_objects, hierarchy=hierarchy)
# shape_img = pcv.analyze_object(img=img, obj=obj, mask=mask)

# MAC Address of Mi Plant Sensor Bluetooth
dongle_addresses = ['C4:7C:8D:6A:D3:97']

# Interval for querying sensors and take picture
interval = 6

def getPercentage(sensor, poller):
    return round(poller.parameter_value(sensor)/(MI_VALUES[sensor]['max'] - MI_VALUES[sensor]['min'])*100)

for dongle_address in dongle_addresses:
    poller = MiFloraPoller(dongle_address, GatttoolBackend)
    camera = PiCamera()

    while(True):
        camera.start_preview()
        poller.fill_cache()
        time.sleep(interval)
        camera.capture(FLORA_PICS + str(datetime.timestamp(datetime.now())) + '.jpg')
        camera.stop_preview()
        # print(poller.name())
        # print(poller.battery_level())
        # print(poller.firmware_version())        
        # print("Date: {:%d-%b-%Y}".format(datetime.date.today()))
        # print("Temperature: " + str(poller.parameter_value(MI_TEMPERATURE)))
        # print("Light: " + str(poller.parameter_value(MI_LIGHT)))
        # print("Moisture: " + str(poller.parameter_value(MI_MOISTURE)))
        # print("Conductivity: " + str(poller.parameter_value(MI_CONDUCTIVITY)))
        # print("Battery: " + str(poller.parameter_value(MI_BATTERY)))
        with open(FLORA_CSV, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([
                time.strftime("%H:%M:%S-%d-%b-%y",time.gmtime()), #0
                poller.parameter_value(MI_TEMPERATURE), #1
                getPercentage(MI_TEMPERATURE,poller), #2
                poller.parameter_value(MI_LIGHT), #3
                getPercentage(MI_LIGHT,poller), #4
                poller.parameter_value(MI_MOISTURE), #5
                poller.parameter_value(MI_CONDUCTIVITY), #6
                getPercentage(MI_CONDUCTIVITY,poller), #7
                poller.parameter_value(MI_BATTERY)]) #8
