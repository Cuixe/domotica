import threading
from batch.dateutils import *
from batch.domain import Task
import math
from utils import logger
from datetime import timedelta


class Manager:
    QUEUED_TASK = {}
    MAIN_TIMER = None

    def __init__(self):
        pass

    @staticmethod
    def start_tasks():
        logger.info("Manager", msg="Current time: " + datetime.now().strftime(format="%H:%M:%S"))
        logger.info(logger_name="Manager", msg="Starting tasks")
        Task.load()
        tasks = Task.load()
        for key, task in tasks:
            Manager.__create_new_timer_task(task)
        logger.debug(logger_name="Manager", msg="Task created: " + str(len(Manager.QUEUED_TASK)))
        now = datetime.now() + timedelta(days=1)
        tomorrow = datetime(year=now.year, month=now.month, day=now.day, hour=0, minute=0, second=0)
        seconds = get_difference_in_seconds(tomorrow, datetime.now())
        seconds = math.ceil(seconds)
        Manager.MAIN_TIMER = threading.Timer(interval=seconds, function=Manager.start_tasks)
        Manager.MAIN_TIMER.start()
        logger.info(logger_name="Manager", msg="Task will be executed again on " + seconds + " seconds")

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

    @staticmethod
    def __create_new_timer_task(task):
        if str(datetime.today().weekday() + 1) in task.execution_days:
            execution_time = cast_time_to_datetime(task.execution_time)
            current_time = datetime.now()
            seconds = get_difference_in_seconds(execution_time, current_time)
            if seconds > 0:
                seconds = math.ceil(seconds)
                timer = threading.Timer(interval=seconds, function=task.execute_tasks)
                timer.name = "Task_" + str(task.id)
                Manager.QUEUED_TASK[task.id] = timer
                timer.start()
                logger.info(logger_name="Manager", msg=(task.name + " will be executed in " + str(seconds) + "seconds"))
