import threading
import datetime as dt

from properties import start_time, end_time
from text import Text

interval = 60


class Notify(object):
    def __init__(self, tof):
        self._tof = tof
        self._running = False
        self._sent = False
        self._cnt = 0

    def check(self):
        hr = dt.datetime.now().hour
        r = self._tof.get_range()
        print(f'Notify: Range[{r}]')
        if start_time > hr >= end_time:
            if r < 400:
                if not self._sent or self._cnt > 15:
                    Text('Garage Door Open').send()
                    self._sent = True
                    self._cnt = 0
                else:
                    self._cnt += 1
            else:
                self._sent = False
        if self._running:
            timer = threading.Timer(interval, self.check)
            timer.start()

    def start(self):
        self._running = True
        timer = threading.Timer(interval, self.check)
        timer.start()

    def stop(self):
        self._running = False
