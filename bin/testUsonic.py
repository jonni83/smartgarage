#!/usr/bin/env python
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import sys, os.path
sys.path.append(os.path.expanduser('/home/pi/development/smartgarage/src'))
from ConfigParser import ConfigParser
from datetime import datetime, timedelta
import time
import RPi.GPIO as GPIO
from SmartGarage.smartgarage import Relay
from SmartGarage.smartgarage import USonic


configfile = "smartgarage.ini"
config = ConfigParser.ConfigParser()

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

def park_assist(channel):
    usonic = USonic()
    relay = Relay()
    while 1:
        distance = usonic.get_distance()
        # 10 feet
        if distance > 305:
            relay.turn_on_only(relay.green)
        # 1 foot
        elif distance > 95:
            relay.turn_on_only(relay.yellow)
        else:
            relay.turn_on_only(relay.red)
        time.sleep(1)

def distance_threshold(us):
    distance = us.get_distance()
    print("distance is {0}".format(distance))
    # 10 feet
    if distance > 305:
        return 3
    # 1 foot
    elif distance > 95:
        return 2
    else:
        return 1

config.read(configfile)
mode = ConfigSectionMap("General")['mode']
if mode == 'bcm':
    mode = GPIO.BCM
elif mode == 'board':
    mode = GPIO.BOARD
else:
    mode = ''
us = ConfigSectionMap("UltraSonic")
re = ConfigSectionMap("Relay")

usonicleft = USonic(int(us['lefttrigger']), int(us['leftecho']), mode)
# usonicright = USonic(int(us['righttrigger']), int(us['rightecho']), mode)
relay = Relay(int(re['red']), int(re['yellow']), int(re['green']), mode)

while 1:
    left_threshold = distance_threshold(usonicleft)
    print("left threshold is {0}".format(left_threshold))
    # right_threshold = distance_threshold(usonicright)
    # print("right threshold is {0}".format(right_threshold))
    # thresholds = [left_threshold, right_threshold]
    # threshold = min(thresholds)
    threshold = left_threshold
 
    if threshold == 1:
        #red light
        relay.turn_on_only(relay.red)
    elif threshold == 2:
        #yellow light
        relay.turn_on_only(relay.yellow)
    elif threshold == 3:
        #green light
        relay.turn_on_only(relay.green)
    elif threshold == 4:
        #no light
        relay.turn_off_all()
    else:
        #error and no light
        print "Error: Threshold incorrectly set"
        relay.turn_off_all()

    time.sleep(1)
