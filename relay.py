import threading

import RPi.GPIO as GPIO

#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)


class Relay(object):
    def __init__(self, pin):
        self._on = False
        self._pin = pin
        self._delay = 1
        GPIO.setup(self._pin, GPIO.OUT)
        GPIO.output(self._pin, GPIO.LOW)

    def set_pin(self, pin):
        self._pin = pin
        GPIO.setup(self._pin, GPIO.OUT)
        GPIO.output(self._pin, GPIO.LOW)

    def set_delay(self, delay_in):
        self._delay = delay_in

    def on(self):
        # TODO turn on
        self._on = True
        GPIO.output(self._pin, GPIO.HIGH)
        timer = threading.Timer(self._delay, self.off)
        timer.start()

    def off(self):
        # TODO turn off
        self._on = False
        GPIO.output(self._pin, GPIO.LOW)
