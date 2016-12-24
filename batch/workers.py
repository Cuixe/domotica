import threading
from batch.dateutils import *
from batch.domain import Task
import math
from collections import OrderedDict
from utils import logger
from datetime import timedelta


class TaskManager:
    QUEUED_TIMER_TASKS = {}
    BEFORE_TASKS = {}
    MAIN_TIMER = None

    def __init__(self):
        pass

    @staticmethod
    def start_tasks():
        logger.info(logger_name="Manager", msg="Starting tasks")
        Task.load()
        tasks = Task.load()
        for task in tasks:
            TaskManager.__create_new_timer_task(task)
        logger.debug(logger_name="Manager", msg="Task created: " + str(len(TaskManager.QUEUED_TIMER_TASKS)))
        logger.debug(logger_name="Manager", msg="Task executed: " + str(len(TaskManager.BEFORE_TASKS)))
        TaskManager.BEFORE_TASKS = OrderedDict(sorted(TaskManager.BEFORE_TASKS.items()))
        TaskManager.execute_before_task()
        now = datetime.now() + timedelta(days=1)
        tomorrow = datetime(year=now.year, month=now.month, day=now.day, hour=0, minute=0, second=0)
        seconds = get_difference_in_seconds(tomorrow, datetime.now())
        seconds = math.ceil(seconds)
        TaskManager.MAIN_TIMER = threading.Timer(interval=seconds, function=TaskManager.start_tasks)
        TaskManager.MAIN_TIMER.start()
        logger.info(logger_name="Manager", msg="Manager Task will be executed again on " + seconds + " seconds")

    @staticmethod
    def update_task(task_id=None, async=True):
        if async:
            timer = threading.Timer(1, TaskManager.update_task, [task_id, False])
            timer.start()
        else:
            if task_id in TaskManager.QUEUED_TIMER_TASKS:
                TaskManager.QUEUED_TIMER_TASKS[task_id].cancel()
                del TaskManager.QUEUED_TIMER_TASKS[task_id]
            task = Task.get_task(task_id=task_id)
            TaskManager.__create_new_timer_task(task)
            TaskManager.execute_before_task()

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
                TaskManager.QUEUED_TIMER_TASKS[task.id] = timer
                timer.start()
                logger.info(logger_name="Manager", msg=(task.name + " will be executed in " + str(seconds) +
                            "seconds and will execute " + str(len(task.events)) + " tasks"))
            else:
                if seconds not in TaskManager.BEFORE_TASKS:
                    seconds += -.00001
                    TaskManager.BEFORE_TASKS[seconds] = task

    @staticmethod
    def execute_before_task():
        TaskManager.BEFORE_TASKS = OrderedDict(sorted(TaskManager.BEFORE_TASKS.items()))
        for key, task in TaskManager.BEFORE_TASKS.iteritems():
            task.execute_tasks()
            logger.info(logger_name="Manager", msg=(task.name + " was already executed "))
            del TaskManager.BEFORE_TASKS[key]
