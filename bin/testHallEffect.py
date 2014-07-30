#!/usr/bin/env python
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import sys, os.path
sys.path.append(os.path.expanduser('/home/pi/development/smartgarage/src'))
import ConfigParser
import RPi.GPIO as GPIO
import time
from SmartGarage.smartgarage import HallEffectPair
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
he = ConfigSectionMap("HallEffect")
re = ConfigSectionMap("Relay")

heleft = HallEffectPair(int(he['leftopen']), int(he['leftclosed']), mode)
heright = HallEffectPair(int(he['rightopen']), int(he['rightclosed']), mode)
relay = Relay(int(re['red']), int(re['yellow']), int(re['green']), mode)

def leftopen(channel):
    print "left door open"
    relay.turn_on_only(relay.green)

def leftclosed(channel):
    print "left door closed"
    relay.turn_on_only(relay.red)

def rightopen(channel):
    print "right door open"
    relay.turn_on_only(relay.green)
    relay.turn_on(relay.yellow)

def rightclosed(channel):
    print "right door closed"
    relay.turn_on_only(relay.red)
    relay.turn_on(relay.yellow)

heleft.add_event_detect(channel=heleft.open_door, callback=leftopen)
heleft.add_event_detect(channel=heleft.closed_door, callback=leftclosed)

heright.add_event_detect(channel=heright.open_door, callback=rightopen)
heright.add_event_detect(channel=heright.closed_door, callback=rightclosed)

while 1:
	time.sleep(5)
