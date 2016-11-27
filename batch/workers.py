import threading
from batch.dateutils import *
from batch.domain import Task
import math
from collections import OrderedDict
from utils import logger


class Manager:
    __QUEUED_TASK = {}
    BEFORE_TASKS = {}

    def __init__(self):
        pass

    def start_tasks(self):
        tasks = Task.get_task_list()
        for task in tasks:
            Manager.__create_new_timer_task(task)
        logger.debug(logger_name="Manager", msg="Task created: " + str(len(Manager.__QUEUED_TASK)))
        logger.debug(logger_name="Manager", msg="Task executed: " + str(len(Manager.BEFORE_TASKS)))
        Manager.BEFORE_TASKS = OrderedDict(sorted(Manager.BEFORE_TASKS.items()))
        Manager.execute_before_task()

    def update_task(self, task_id):
        Manager.__QUEUED_TASK[task_id].cancel()
        task = Task.get_task(task_id, update=True)
        Manager.__create_new_timer_task(task)
        Manager.execute_before_task()

    @staticmethod
    def __create_new_timer_task(task):
        if str(datetime.today().weekday() + 1) in task.execution_days:
            execution_time = cast_time_to_datetime(task.execution_time)
            seconds = get_difference_in_seconds(execution_time, datetime.now())
            if seconds > 0:
                seconds = math.ceil(seconds)
                timer = threading.Timer(interval=seconds, function=task.execute_tasks)
                timer.name = "Task_" + str(task.id)
                Manager.__QUEUED_TASK[task.id] = timer
                timer.start()
                logger.info(logger_name="Manager", msg=(task.name + " will be executed in " + str(seconds) + "seconds"))
            else:
                if seconds not in Manager.BEFORE_TASKS:
                    seconds += -.00001
                    Manager.BEFORE_TASKS[seconds] = task

    @staticmethod
    def execute_before_task():
        Manager.BEFORE_TASKS = OrderedDict(sorted(Manager.BEFORE_TASKS.items()))
        for key, task in Manager.BEFORE_TASKS.iteritems():
            task.execute_tasks()
            logger.info(logger_name="Manager", msg=(task.name + " was already executed "))
