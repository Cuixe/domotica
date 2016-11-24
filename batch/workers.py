import threading, time
from batch.models.SocketTask import SocketTask
from batch.dateutils import *


class TaskManager:
    TASKS = []
    MANAGER=None

    def __init__(self):
        TaskManager.MANAGER = Manager()
        TaskManager.MANAGER.start()


class Manager(threading.Thread):

    def __init__(self, sleep_time=1):
        threading.Thread.__init__(self, name="MANAGER")
        self.tasks = SocketTask.get_socket_tasks()
        self.sleep_time = sleep_time
        self.queued_tasks = {}

    def invoque(self, task):
        if task.new_status:
            task.socket.turn_on()
            print task.socket.name + " turned on"
        else:
            task.socket.turn_off()
            print task.socket.name + " turned off"

    def run(self):
        i = 1
        day = datetime.today().weekday() + 1
        now = datetime.now()
        index = 0;
        while index < len(self.tasks):
            task = self.tasks[index];
            if str(day) in task.frequency:
                execution_time = cast_time_to_datetime(task.execution_time)
                seconds = get_seconds_diff_between_datetime(execution_time, now)
                i += 1
                seconds = i
                if seconds > 0:
                    timer = threading.Timer(seconds, self.invoque, (task,))
                    self.queued_tasks[task.socket.name] = timer
                    timer.start()
            index += 1
