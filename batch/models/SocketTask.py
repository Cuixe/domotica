import datetime


class SocketTask(object):
    def __init__(self, socket=None, execution_time=datetime.time.dst(), new_status=False, frequency=""):
        self.socket = socket
        self.execution_time = execution_time
        self.new_status = new_status
        self.frequency = frequency
