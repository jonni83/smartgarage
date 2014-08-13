#!/usr/bin/env python
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import sys
import os.path
sys.path.append(os.path.expanduser('/home/pi/development/smartgarage/src'))
from ConfigParser import ConfigParser
import RPi.GPIO as GPIO
import zerorpc
from SmartGarage.smartgarage import USonic
from SmartGarage.smartgarage import HallEffectPair
import faulthandler
faulthandler.enable()
import logging
logging.basicConfig()


class GarageServer(object):
    def _ConfigSectionMap(self, config, section):
        print "mapping config"
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

    def _getConfig(self):
        print "getting config"
        configfile = "/home/pi/development/smartgarage/smartgarage.ini"
        config = ConfigParser.ConfigParser()
        config.read(configfile)
        return config

    def _getMode(self, config):
        print "getting mode"
        mode = self._ConfigSectionMap(config, "General")['mode']
        if mode == 'bcm':
            mode = GPIO.BCM
        elif mode == 'board':
            mode = GPIO.BOARD
        else:
            mode = ''

        return mode

    def isDoorOpen(self, door):
        """Checks to see if the specified `door` is open.

        Parameters
        ----------
        door : str
            Acceptable values are right or left, otherwise object
            defaults will be used.

        Returns
        -------
        bool
            True for open
            False for closed
        """
        print "starting door open function"
        config = self._getConfig()
        mode = self._getMode(config)
        he = self._ConfigSectionMap(config, "HallEffect")

        if door == "right":
            # setup right sensor
            opened = int(he['rightopen'])
            closed = int(he['rightclosed'])
        elif door == "left":
            # setup left sensor
            opened = int(he['leftopen'])
            closed = int(he['leftclosed'])

        print "creating sensor object"
        print(opened, closed, mode)
        halleffect = HallEffectPair(opened, closed, mode)

        print "reading the state and returning"
        if halleffect.get_state(opened):
            print "yes"
            return "yes"
        else:
            print "no"
            return "no"

    def isBayOccupied(self, door):
        """Checks to see if the specified `bay` is open.

        Parameters
        ----------
        door : str
            Acceptable values are right or left, otherwise object
            defaults will be used.

        Returns
        -------
        bool
            True for occupied
            False for empty
        """
        config = self._getConfig()
        mode = self._getMode(config)
        us = self._ConfigSectionMap(config, "UltraSonic")

        if door == "right":
            # setup right sensor
            trigger = int(us['righttrigger'])
            echo = int(us['rightecho'])
        elif door == "left":
            # setup left sensor
            trigger = int(us['lefttrigger'])
            echo = int(us['leftecho'])

        usonic = USonic(trigger, echo, mode)

        if usonic.get_distance() < 305:
            return True
        else:
            return False

    def hello(self, name):
        """Serves to test functionality.
        Parameters
        ----------
        name : str

        Returns
        -------
        str
            composition is - hello `name`
        """
        return "hello {0}".format(name)


s = zerorpc.Server(GarageServer())
s.bind("tcp://0.0.0.0:4242")
s.run()
