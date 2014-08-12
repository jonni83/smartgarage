#!/usr/bin/env python
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import sys
import os.path
sys.path.append(os.path.expanduser('/home/pi/development/smartgarage/src'))
import ConfigParser
from datetime import datetime, timedelta
import time
import RPi.GPIO as GPIO
from SmartGarage.smartgarage import Relay
from SmartGarage.smartgarage import USonic
from SmartGarage.smartgarage import HallEffectPair


configfile = "smartgarage.ini"
config = ConfigParser.ConfigParser()
left_open_time = datetime.now() - timedelta(minutes=1)
right_open_time = datetime.now() - timedelta(minutes=1)


def ConfigSectionMap(section):
    """Create a dict out of any section of a config file.

    Args:
        section: name of the section

    Returns:
        dict: key/value pairs of each entry within the section
    """
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                print("skip: {0}".format(option))
        except:
            "exception on {0}!".format(option)
            dict1[option] = None
    return dict1


def set_left_time(channel):
    """Set the global timestamp for the last time
    the left garage bay door was opened. This is meant to be used
    inside a GPIO callback.

    Args:
        channel: Not used, required in function defintion by GPIO.
    """
    global left_open_time
    left_open_time = datetime.now()


def set_right_time(channel):
    """Set the global timestamp for the last time
    the left garage bay door was opened. This is meant to be used
    inside a GPIO callback.

    Args:
        channel: Not used, required in function defintion by GPIO.
    """
    global right_open_time
    right_open_time = datetime.now()


def distance_threshold(time, us):
    """Determines the threshold that has been reached by the car.

    Args:
        time: the timestamp for when the door was last opened
        us: the ultrasonic sensor that is being observed

    Returns:
        4 if garage door has been open for a while
        3 if the distance is over 10 ft
        2 if the distance is over 1 ft
        1 if the distance is 1 ft or less
    """
    if datetime.now()-time > timedelta(seconds=60):
        return 4

    distance = us.get_distance()
    # 10 feet
    if distance > 305:
        return 3
    # 1 foot
    elif distance > 95:
        return 2
    else:
        return 1


if __name__ == "__main__":
    """Read the config parameters, initialize all the sensors,
    and loop the logic show the proper light.
    """
    config.read(configfile)
    mode = ConfigSectionMap("General")['mode']
    if mode == 'bcm':
        mode = GPIO.BCM
    elif mode == 'board':
        mode = GPIO.BOARD
    else:
        mode = ''
    he = ConfigSectionMap("HallEffect")
    us = ConfigSectionMap("UltraSonic")
    re = ConfigSectionMap("Relay")

    halleffectleft = HallEffectPair(int(he['leftopen']), int(he['leftclosed']),
                                    mode)
    halleffectright = HallEffectPair(int(he['rightopen']),
                                     int(he['rightclosed']), mode)
    ultrasonicleft = USonic(int(us['lefttrigger']), int(us['leftecho']), mode)
    ultrasonicright = USonic(int(us['righttrigger']), int(us['rightecho']),
                             mode)
    relay = Relay(int(re['red']), int(re['yellow']), int(re['green']), mode)

    halleffectleft.add_event_detect(channel=halleffectleft.open_door,
                                    callback=set_left_time)
    halleffectright.add_event_detect(channel=halleffectright.open_door,
                                     callback=set_right_time)

    while 1:
        left_threshold = distance_threshold(left_open_time, ultrasonicleft)
        right_threshold = distance_threshold(right_open_time, ultrasonicright)
        thresholds = [left_threshold, right_threshold]
        threshold = min(thresholds)

        if threshold == 1:
            # red light
            relay.turn_on_only(relay.red)
        elif threshold == 2:
            # yellow light
            relay.turn_on_only(relay.yellow)
        elif threshold == 3:
            # green light
            relay.turn_on_only(relay.green)
        elif threshold == 4:
            # no light
            relay.turn_off_all()
        else:
            # error and no light
            print "Error: Threshold incorrectly set"
            relay.turn_off_all()
