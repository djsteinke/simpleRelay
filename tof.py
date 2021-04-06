import time
import threading
import VL53L0X.python.VL53L0X as VL53L0X


class TOF(object):
    def __init__(self):
        self._running = False
        self._range = 0
        self._delay = 10
        self._sensor = VL53L0X.VL53L0X(i2c_bus=3, i2c_address=0x29)

    def get_range(self):
        self._sensor.open()
        self._sensor.start_ranging(VL53L0X.V15310xAccuracyMode.BEST)
        timing = self._sensor.get_timing()
        if timing < 20000:
            timing = 20000
        tot = 0
        cnt = 0
        t_cnt = 0
        while cnt < 3:
            distance = self._sensor.get_distance()
            if distance > 0:
                tot += distance
                cnt += 1
            t_cnt += 1
            if t_cnt > 100:
                break
            time.sleep(timing/1000000.0)
        self._sensor.stop_ranging()
        self._sensor.close()
        avg = 0
        if cnt > 0:
            avg = tot/cnt
        return avg

    def run(self):
        while self._running:
            self._range = self.get_range()
            timer = threading.Timer(self._delay, self.run)
            timer.start()

    def start(self):
        if not self._running:
            self._running = True
            self.run()

    def stop(self):
        self._running = False

    @property
    def range(self):
        return self._range

