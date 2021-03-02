import logging
import socket
import threading

import RPi.GPIO as GPIO

from flask import Flask, request, jsonify, send_from_directory

from relay import Relay
from static import get_logging_level
import os

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

relay = Relay(0)


@app.route('/relay/<pin_in>/<action>/<time>')
def relay_action(pin_in, action, time):
    logger.debug(f"relay[{pin_in}] action[{action}] time[{time}]")
    i_time = int(time)
    relay.set_pin(int(pin_in))
    if action == "on":
        relay.on()
        if i_time > 0:
            timer = threading.Timer(i_time, relay.off())
            timer.start()
    else:
        relay.off()
    # pin_state = GPIO.input(pin)
    return jsonify(message="Success",
                   statusCode=200,
                   data=action), 200


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    host_name = socket.gethostbyname(socket.gethostname())
    logger.info("machine host_name[" + host_name + "]")
    print(host_name + "[" + host_name[0: 3] + "]")
    if host_name[0: 3] == "192" or host_name[0: 3] == "127":
        host_name = "192.168.0.140"
    else:
        host_name = "localhost"
    logger.info("app host_name[" + host_name + "]")
    # app.run(ssl_context='adhoc', host=host_name, port=1983)
    app.run(host=host_name, port=1983)
