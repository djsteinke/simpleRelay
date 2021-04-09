import logging
import socket
import threading
import datetime as dt

import RPi.GPIO as GPIO

from flask import Flask, jsonify, send_from_directory

from relay import Relay
from static import get_logging_level
from properties import ip, port, end_time, start_time
import os

from tof import TOF

app = Flask(__name__)

# create logger with 'spam_application'
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('log.log')
fh.setLevel(get_logging_level())
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

tof = TOF()


@app.route('/relay/<pin_in>')
def relay_action(pin_in):
    logger.debug(f"relay[{pin_in}] action[ON] time[1]")
    status = 200
    relay = Relay(int(pin_in))
    relay.on()
    return jsonify(message="Success",
                   statusCode=status), status


@app.route('/door/<action>')
def door(action):
    global tof
    logger.info(f"door({action})")
    val = action
    if action == 'on':
        tof.start()
    elif action == 'off':
        tof.stop()
    elif action == 'get':
        val = tof.range
    elif action == 'status':
        val = tof.get_status()
    else:
        val = "Invalid action"
    return {"value": val}, 200


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    host_name = socket.gethostbyname(socket.gethostname())
    logger.info("machine host_name[" + host_name + "]")
    print(host_name + "[" + host_name[0: 3] + "]")
    if host_name[0: 3] == "192" or host_name[0: 3] == "127":
        host_name = ip
    else:
        host_name = "localhost"
    logger.info("app host_name[" + host_name + "]")
    # app.run(ssl_context='adhoc', host=host_name, port=1983)
    tof.start()
    app.run(host=host_name, port=port)
