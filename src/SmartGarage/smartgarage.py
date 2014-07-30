#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import RPi.GPIO as GPIO
from time import time, sleep

class Component(object):
    def __init__(self, mode):
        self.setmode(mode)

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

        super(Relay, self).__init__(mode)

        self.red = red
        self.yellow = yellow
        self.green = green

        for pin in self.red, self.yellow, self.green:
            GPIO.setup(pin, GPIO.OUT, Relay.LIGHT_OFF)

    def turn_off(self, color):
        if color not in [self.red, self.yellow, self.green]:
            return

        GPIO.output(color, Relay.LIGHT_OFF)

    def turn_off_all(self):
        for pin in self.red, self.yellow, self.green:
            GPIO.output(pin, Relay.LIGHT_OFF)

    def turn_on(self, color):
        if color not in [self.red, self.yellow, self.green]:
            return
        
        sleep(.5)

        GPIO.output(color, Relay.LIGHT_ON)
        
    def turn_on_only(self, color):
        """ Turn on only the color light specified.
        There is a built-in software debounce which is actually attempting to mitigate
        a potential ground loop problem."""

        """ validate input """
	if color not in [self.red, self.yellow, self.green]:
	    return

        # software debouce: wait .5 seconds
        sleep(.5)

	self.turn_off_all()

        GPIO.output(color, Relay.LIGHT_ON)


class USonic(Component):
    def __init__(self, trigger=7, echo=8, mode=GPIO.BCM):
        """ Defines the GPIO channels for an ultrasonic distance sensor.
        The default channel of the trigger pin is 22.
        The default channel of the echo pin is 25.
        The default board mode is set to GPIO.BCM."""

        super(USonic, self).__init__(mode)
        
        self.trigger = trigger
        self.echo = echo

        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

        # sensor must be primed to function properly
        GPIO.output(self.trigger, GPIO.LOW)
        sleep(0.3)

    def get_distance(self):
        """ Get distance measured in centimeters"""

        GPIO.output(self.trigger, GPIO.LOW)
        sleep(0.3)

        GPIO.output(self.trigger, True)
        sleep(0.00001)
        GPIO.output(self.trigger, False)

        signal_start = 0
        signal_stop = 0

        # wait for signal to start
        while GPIO.input(self.echo) == 0:
            signal_start = time()

        # wait for signal to stop
        while GPIO.input(self.echo) == 1:
            signal_stop = time()

        time_passed = signal_stop - signal_start

        return time_passed * 17000


class HallEffectPair(Component):
    def __init__(self, open_door=17, closed_door=4, mode=GPIO.BCM):
        """ Defines the GPIO channels for reading the status of two hall effect sensors.
        The default channel of the sensor for the open position is 17.
        The default channel of the sensor for the closed position is 4.
        The default board mode is set to GPIO.BCM."""

        super(HallEffectPair, self).__init__(mode)

        self.open_door = open_door
        self.closed_door = closed_door

        GPIO.setup(self.open_door, GPIO.IN)
        GPIO.setup(self.closed_door, GPIO.IN)

    def add_event_detect(self, channel, callback):
        GPIO.add_event_detect(channel, GPIO.FALLING, callback=callback, bouncetime=2000)

    def get_state(self, channel):
        return GPIO.input(channel)
