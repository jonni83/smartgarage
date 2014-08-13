#!/usr/bin/env python

from ConfigParser import ConfigParser
import RPi.GPIO as GPIO
import time
from SmartGarage.smartgarage import HallEffectPair
from SmartGarage.smartgarage import Relay

configfile = "smartgarage.ini"
config = ConfigParser.ConfigParser()
config.read(configfile)

mode = ConfigSectionMap("General")['mode']
he = ConfigSectionMap("HallEffect")

heleft = HallEffectPair(int(he['leftopen']), int(he['leftclosed']), mode)
heright = HallEffectPair(int(he['rightopen']), int(he['rightclosed']), mode)
relay = Relay(int(re['red']), int(re['yellow']), int(re['green']), mode)

GPIO.add_event_detect(HallEffectPair.OPENDOOR, GPIO.FALLING, callback=turnongreen, bouncetime=1000)
GPIO.add_event_detect(HallEffectPair.CLOSEDDOOR, GPIO.FALLING, callback=turnonred, bouncetime=1000)

while 1:
	print "turning on yellow light"
	turnonlight(Relay.YELLOW)
	time.sleep(5)
