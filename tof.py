import time
import threading
import VL53L0X.python.VL53L0X as VL53L0X
import logging

logger = logging.getLogger('main.program')


class TOF(object):
    def __init__(self):
        self._running = False
        self._range = 0
        self._delay = 60

    def get_range(self):
        logger.debug("get_range()")
        sensor = VL53L0X.VL53L0X(i2c_bus=3,i2c_address=0x29)
        sensor.open()
        sensor.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BEST)
        timing = sensor.get_timing()
        if timing < 20000:
            timing = 20000
        tot = 0
        cnt = 0
        t_cnt = 0
        while cnt < 3:
            distance = sensor.get_distance()
            if distance > 0:
                logger.debug("measured: " + distance)
                tot += distance
                cnt += 1
            t_cnt += 1
            if t_cnt > 100:
                break
            time.sleep(timing/1000000.0)
        sensor.stop_ranging()
        sensor.close()
        if cnt > 0:
            avg = tot/cnt
            self._range = avg

    def get_status(self):
        if self._running:
            return "running"
        else:
            return "stopped"

    def run(self):
        while self._running:
            logger.debug("run()")
            self.get_range()
            timer = threading.Timer(self._delay, self.run)
            timer.start()

    def start(self):
        if not self._running:
            logger.debug("start()")
            self._running = True
            timer = threading.Timer(0, self.run)
            timer.start()

    def stop(self):
        self._running = False

    @property
    def range(self):
        return self._range

