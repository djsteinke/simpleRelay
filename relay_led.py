import threading
from gpiozero import LED


class RelayLED(object):
    def __init__(self, pin):
        self._delay = 1
        self._on = False
        self._led = LED(pin=pin, initial_value=None)

    def set_delay(self, delay_in):
        self._delay = delay_in

    def toggle(self):
        self._led.toggle()
        if not self._on:
            timer = threading.Timer(self._delay, self.toggle)
            timer.start()
            self._on = True
        else:
            self._on = False


