import threading
from batch.dateutils import *
from batch.domain import Task
import math
from collections import OrderedDict
from utils import logger


class Manager:
    QUEUED_TASK = {}
    BEFORE_TASKS = {}

    def __init__(self):
        pass

    @staticmethod
    def start_tasks():
        tasks = Task.get_task_list()
        for task in tasks:
            Manager.__create_new_timer_task(task)
        logger.debug(logger_name="Manager", msg="Task created: " + str(len(Manager.QUEUED_TASK)))
        logger.debug(logger_name="Manager", msg="Task executed: " + str(len(Manager.BEFORE_TASKS)))
        Manager.BEFORE_TASKS = OrderedDict(sorted(Manager.BEFORE_TASKS.items()))
        Manager.execute_before_task()


    @staticmethod
    def update_task(task_id=None, async=True):
        if async:
            timer = threading.Timer(1, Manager.update_task, [task_id, False])
            timer.start()
        else:
            if task_id in Manager.QUEUED_TASK:
                Manager.QUEUED_TASK[task_id].cancel()
                del Manager.QUEUED_TASK[task_id]
            task = Task.get_task(task_id=task_id, update=True)
            Manager.__create_new_timer_task(task)
            Manager.execute_before_task()

    @staticmethod
    def __create_new_timer_task(task):
        if str(datetime.today().weekday() + 1) in task.execution_days:
            execution_time = cast_time_to_datetime(task.execution_time)
            current_time = datetime.now()
            logger.info("Manager", msg="Current time: " + current_time.strftime(format="%H:%M:%S"))
            seconds = get_difference_in_seconds(execution_time, current_time)
            if seconds > 0:
                seconds = math.ceil(seconds)
                timer = threading.Timer(interval=seconds, function=task.execute_tasks)
                timer.name = "Task_" + str(task.id)
                Manager.QUEUED_TASK[task.id] = timer
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
            del Manager.BEFORE_TASKS[key]
