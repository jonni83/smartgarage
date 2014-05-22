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

    """ unintuitive mapping """
    LIGHT_ON = GPIO.LOW
    LIGHT_OFF = GPIO.HIGH

    def __init__(self, red=24, yellow=23, green=18, mode=GPIO.BCM):
        """ Defines the GPIO channels for the lights in the stoplight connected
        to a 4-channel relay.
        The default channel of the red light is 24.
        The default channel of the yellow light is 23.
        The default channel of the green light is 18.
        The default board mode is set to GPIO.BCM."""

        self.setmode(mode)

        self.red = red
        self.yellow = yellow
        self.green = green

        for pin in self.red, self.yellow, self.green:
            GPIO.setup(pin, GPIO.OUT, LIGHT_OFF)

    def turn_on_only(self, color):
        """ Turn on only the color light specified.
        There is a built-in software debounce which is actually attempting to mitigate
        a potential ground loop problem."""

        """ validate input """
	if color not in [self.red, self.yellow, self.green]:
	    return

        # software debouce: wait .5 seconds
        time.sleep(.5)

        for pin in self.red, self.yellow, self.green:
            GPIO.output(pin, LIGHT_OFF)

        GPIO.output(color, LIGHT_ON)


class USonic(Component):
    def __init__(self, TRIGGER=7, ECHO=8, mode=GPIO.BCM):
        """ Defines the GPIO channels for an ultrasonic distance sensor.
        The default channel of the trigger pin is 22.
        The default channel of the echo pin is 25.
        The default board mode is set to GPIO.BCM."""

        self.setmode(mode)
        
        self.trigger = TRIGGER
        self.echo = ECHO

        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

        # sensor must be primed to function properly
        GPIO.output(self.trigger, GPIO.LOW)
        time.sleep(0.3)

    def get_distance(self):
        """ Get distance measured in centimeters"""

        GPIO.output(self.trigger, GPIO.LOW)
        time.sleep(0.3)

        GPIO.output(self.trigger, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger, False)

        signalon = 0
        signaloff = 0

        # wait for signal to start
        while GPIO.input(self.echo) == 0:
            signalstart = time.time()

        # wait for signal to stop
        while GPIO.input(self.echo) == 1:
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

        self.open_door = OPENDOOR
        self.closed_door = CLOSEDDOOR

        GPIO.setup(self.open_door, GPIO.IN)
        GPIO.setup(self.closed_door, GPIO.IN)

    def add_event_detect(self, channel, callback):
        GPIO.add_event_detect(channel, GPIO.FALLING, callback=callback, bouncetime=1000)
