# Based on Raspbian Buster
# sudo su
# apt-get update -y
# apt-get upgrade -y
# apt-get autoremove -y
# apt-get clean -y

# Install https://github.com/jjhelmus/berryconda (armv6l archicture)
# wget -O install-berryconda.sh "https://github-production-release-asset-2e65be.s3.amazonaws.com/75886189/cee3b8a8-5fd0-11e7-9c4d-49e02b8d9630?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20190827%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20190827T190041Z&X-Amz-Expires=300&X-Amz-Signature=fc61660a227a9486ba0fe81806b6319957844a139c4b6f950c69c95a07505433&X-Amz-SignedHeaders=host&actor_id=327285&response-content-disposition=attachment%3B%20filename%3DBerryconda3-2.0.0-Linux-armv6l.sh&response-content-type=application%2Foctet-stream"
# chmod +x install-berryconda.sh && ./install-berryconda.sh -b
# /root/berryconda3/bin/conda create -y -n flora python=3.6 plantcv
# /root/berryconda3/bin/conda activate flora
# cd /root/berryconda3/bin
# ./pip install miflora picamera
# cd /home/pi/flora
# /root/berryconda3/bin/python3 flora.py

from miflora.miflora_poller import MiFloraPoller
from btlewrap.gatttool import GatttoolBackend
import time
import csv
from datetime import datetime
from picamera import PiCamera
from plantcv import plantcv as pcv

FLORA_HOME = '/home/pi/flora'
FLORA_DATA = FLORA_HOME + '/data'
FLORA_PICS = FLORA_DATA + '/pics'
FLORA_CSV = FLORA_DATA + 'flora.csv'

MI_TEMPERATURE = "temperature"
MI_LIGHT = "light"
MI_MOISTURE = "moisture"
MI_CONDUCTIVITY = "conductivity"
MI_BATTERY = "battery"

print('plantcv installed, version' + pcv.__version__)

# MAC Address of Mi Plant Sensor Bluetooth
dongle_addresses = ['C4:7C:8D:6A:D3:97']

# Interval for querying sensors and take picture
interval = 600

for dongle_address in dongle_addresses:
    poller = MiFloraPoller(dongle_address, GatttoolBackend)

    # with open('data/flora.csv', 'a', newline='') as csvfile:
    #     writer = csv.writer(csvfile, delimiter=',')
    #     writer.writerow(['date', 'temperature', 'light', 'moisture', 'conductivity', 'battery'])

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
                time.strftime("%H:%M:%S-%d-%b-%y",time.gmtime()),
                poller.parameter_value(MI_TEMPERATURE),
                poller.parameter_value(MI_LIGHT),
                poller.parameter_value(MI_MOISTURE),
                poller.parameter_value(MI_CONDUCTIVITY),
                poller.parameter_value(MI_BATTERY)])