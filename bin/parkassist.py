#!/usr/bin/env python
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import ConfigParser
import RPi.GPIO as GPIO
from SmartGarage.smartgarage import Relay
from SmartGarage.smartgarage import USonic
from SmartGarage.smartgarage import HallEffectPair



configfile = "smartgarage.ini"

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

def park_assist(channel):
    usonic = USonic()
    relay = Relay()
    while 1:
        distance = usonic.get_distance()
        # 10 feet
        if distance > 305:
            relay.turn_on_only(relay.GREEN)
        # 1 foot
        elif distance > 95:
            relay.turn_on_only(relay.YELLOW)
        else:
            relay.turn_on_only(relay.RED)
        time.sleep(1)

def wait_for_door():
    halleffectpair = HallEffectPair()
    halleffectpair.add_event_detect(channel=halleffectpair.OPENDOOR, callback=park_assist)
    
    while 1:
        time.sleep(600)

if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    config.read(configfile)
    wait_for_door()
