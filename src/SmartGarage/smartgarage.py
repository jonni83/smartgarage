#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import RPi.GPIO as GPIO
import time

class Component(object):
    def setmode(self, mode):
       """ set the mode of the GPIO board to either BOARD or BCM"""
       GPIO.setmode(mode)
	
    def cleanup(self):
        """ Frees the pins.  This avoids errors if the service is restarted."""
        GPIO.cleanup()


class Relay(Component):

    def __init__(self, red=24, yellow=23, green=18, mode=GPIO.BCM):
        """ Defines the GPIO channels for the lights in the stoplight connected
        to a 4-channel relay.
        The default channel of the red light is 24.
        The default channel of the yellow light is 23.
        The default channel of the green light is 18.
        The default board mode is set to GPIO.BCM."""

        self.setmode(mode)

        self.LIGHTON = GPIO.LOW
        self.LIGHTOFF = GPIO.HIGH
        self.RED = red
        self.YELLOW = yellow
        self.GREEN = green

        for pin in self.RED, self.YELLOW, self.GREEN:
            GPIO.setup(pin, GPIO.OUT, self.LIGHTOFF)

    def turn_on_only(self, color):
        """ Turn on only the color light specified.
        There is a built-in software debounce which is actually attempting to mitigate
        a potential ground loop problem."""

        # software debouce: wait .5 seconds
        time.sleep(.5)

        for pin in self.RED, self.YELLOW, self.GREEN:
            GPIO.output(pin, self.LIGHTOFF)

        GPIO.output(color, self.LIGHTON)


class USonic(Component):
    def __init__(self, TRIGGER=7, ECHO=8, mode=GPIO.BCM):
        """ Defines the GPIO channels for an ultrasonic distance sensor.
        The default channel of the trigger pin is 22.
        The default channel of the echo pin is 25.
        The default board mode is set to GPIO.BCM."""

        self.setmode(mode)
        
        self.TRIGGER = TRIGGER
        self.ECHO = ECHO

        GPIO.setup(self.TRIGGER, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)

        # sensor must be primed to function properly
        GPIO.output(self.TRIGGER, GPIO.LOW)
        time.sleep(0.3)

    def get_distance(self):
        """ Get distance measured in centimeters"""

        GPIO.output(self.TRIGGER, GPIO.LOW)
        time.sleep(0.3)

        GPIO.output(self.TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIGGER, False)

        signalon = 0
        signaloff = 0

        # wait for signal to start
        while GPIO.input(self.ECHO) == 0:
            signalstart = time.time()

        # wait for signal to stop
        while GPIO.input(self.ECHO) == 1:
            signalstop = time.time()

        timepassed = signalstop - signalstart

        return timepassed * 17000


class HallEffectPair(Component):
    def __init__(self, OPENDOOR=17, CLOSEDDOOR=4, mode=GPIO.BCM):
        """ Defines the GPIO channels for reading the status of two hall effect sensors.
        The default channel of the sensor for the open position is 17.
        The default channel of the sensor for the closed position is 4.
        The default board mode is set to GPIO.BCM."""

        self.setmode(mode)

        self.OPENDOOR = OPENDOOR
        self.CLOSEDDOOR = CLOSEDDOOR

        GPIO.setup(self.OPENDOOR, GPIO.IN)
        GPIO.setup(self.CLOSEDDOOR, GPIO.IN)

    def add_event_detect(self, channel, callback):
        GPIO.add_event_detect(channel, GPIO.FALLING, callback=callback, bouncetime=1000)
