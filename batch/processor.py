from batch.networking import Message
from utils import raspberry
from batch.domain import Pin, Task


def process_message(message=None):
    if message is None:
        raise Exception("Message can't be None")
    if message.element == 'pin':
        __process_pin(message)
    elif message.element == 'task':
        __process_task(message)


def __process_pin(message=None):
    pin = Pin.get_pin(message.id)
    if message.status == "turnOn":
        raspberry.turn_on_pin(pin.pin_number)
    if message.status == "turnOff":
        raspberry.turn_off_pin(pin.pin_number)


def __process_task(message=None):
    task = Task.get_task(pin_id=message.id, update=True)
    task
    pass