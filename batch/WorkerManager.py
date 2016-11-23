import threading
task_list = []


class WorkerManager(object):
    workers = []
    Threads = []
    #sockedWorkerDao = SocketWorkerDao()

    def reload_workers(self):
        self.workers = self.sockedWorkerDao.get_workers()


class Worker(threading.Timer):
    socket_worker = None
    time_to_next_execution = -1

    def __init__(self, socket_worker=None):
        self.socket_worker = socket_worker
        socket_worker.execution_time
        self.timer = threading.Timer()

    def operation(self):
        socket = self.socket_worker.socket()
        if self.socket_worker.new_status:
            socket.status = True
        else:
            socket.status = False
