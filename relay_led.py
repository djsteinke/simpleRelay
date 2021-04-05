from gpiozero import LED


class Relay(object):
    def __init__(self, pin):
        self._delay = 0
        self._led = LED(pin)

    def set_pin(self, pin):
        self._led = LED(pin)

    def set_delay(self, delay_in):
        self._delay = delay_in

    def blink(self):
        self._led.blink()

