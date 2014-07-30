#!/usr/bin/env python
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=

import sys, os.path
sys.path.append(os.path.expanduser('/home/pi/development/smartgarage/src'))
import ConfigParser
import RPi.GPIO as GPIO
import time
from SmartGarage.smartgarage import Relay

configfile = "smartgarage.ini"
config = ConfigParser.ConfigParser()
config.read(configfile)

def ConfigSectionMap(section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
	    if dict1[option] == -1:
                DebugPrint("skip: {0}".format(option))
        except:
            "exception on {0}!".format(option)
	    dict1[option] = None
    return dict1

mode = ConfigSectionMap("General")['mode']
if mode == 'bcm':
    mode = GPIO.BCM
elif mode == 'board':
    mode = GPIO.BOARD
else:
    mode = ''

re = ConfigSectionMap("Relay")

relay = Relay(int(re['red']), int(re['yellow']), int(re['green']), mode)

while True:
    relay.turn_on_only(relay.red)
    time.sleep(1)
    relay.turn_on_only(relay.yellow)
    time.sleep(1)
    relay.turn_on_only(relay.green)
    time.sleep(1)
