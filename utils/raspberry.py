from utils import logger
"""import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
"""


def call_pin(pin_number=0, status=False):
    logger.info(logger_name="GPIO", msg="Pin: " + str(pin_number) + " sending " + str(status))
    """GPIO.setup(logger_name, GPIO.OUT)
    if status :
        GPIO.output(logger_name, GPIO.HIGH)
    else:
        GPIO.output(logger_name, GPIO.LOW)
"""