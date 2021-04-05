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
        timer = threading.Timer(self._delay, self.reset)
        timer.start()

    def reset(self):
        self._led.toggle()


