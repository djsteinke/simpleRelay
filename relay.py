import threading

import RPi.GPIO as GPIO

#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)


class Relay(object):
    def __init__(self, pin, callback):
        self._on = False
        self._pin = pin
        self._delay = 1
        self._callback = callback
        GPIO.setup(self._pin, GPIO.OUT)
        if GPIO.input(self._pin) == 0:
            self._on_state = GPIO.HIGH
            self._off_state = GPIO.LOW
        else:
            self._on_state = GPIO.LOW
            self._off_state = GPIO.HIGH
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
        GPIO.output(self._pin, self._on_state)
        timer = threading.Timer(self._delay, self.off)
        timer.start()

    def off(self):
        # TODO turn off
        self._on = False
        GPIO.output(self._pin, self._off_state)
        if self._callback is not None:
            self._callback()
