from batch.dao import DataSource
from datetime import datetime
from utils import logger, raspberry


class Domain:

    def __init__(self):
        pass

    def fill(self, *query_result):
        pass


class Pin(Domain):
    __PINS = {}
    __ALL = "SELECT id, pin_number, output, type FROM api_pin"
    __DETAIL = __ALL + " WHERE = %s"
    __UPDATE = "UPDATE api_pin SET output=%s WHERE id=%s"

    def __init__(self, id=None, pin_number=None, output=False, type=None):
        self.id = id
        self.pin_number = pin_number
        self.output = output
        self.type = type

    def __str__(self):
        return "Pin: " + str(self.pin_number)

    def turn_on(self):
        self.output = True
        raspberry.call_pin(self.pin_number, self.output)
        self.__update()
        logger.debug("Pin: " + str(self.pin_number) + " turned on")

    def turn_off(self):
        self.output = False
        raspberry.call_pin(self.pin_number, self.output)
        self.__update()
        logger.debug("Pin: " + str(self.pin_number) + " turned off")

    def fill(self, query_result):
        self.id = query_result[0]
        self.pin_number = query_result[1]
        self.output = query_result[2] == 1
        self.type = query_result[3]

    def __update(self):
        data_source = DataSource.get_instance()
        data_source.execute(Pin.__UPDATE, [1 if self.output else 0, self.id])

    @staticmethod
    def load():
        logger.debug(logger_name="Pin", msg="Loading pins")
        Pin.__PINS.clear()
        data_source = DataSource.get_instance()
        Pin.__PINS = data_source.query_for_dictionary(domain_type=Pin, query=Pin.__ALL)
        logger.info(logger_name="Pin", msg="Pins loaded: " + str(len(Pin.__PINS)))

    @staticmethod
    def get_pin(pin_id):
        logger.debug(logger_name="Pin", msg="Pin requested " + str(pin_id))
        if len(Pin.__PINS) == 0:
            Pin.load()
        return Pin.__PINS[pin_id]


class Event(Domain):
    __EVENTS = {}
    __ALL = "SELECT id, pin_id, name, event_output FROM api_event"
    __DETAIL = __ALL + " WHERE id = %s"

    def __init__(self, id=None, pin_id=None, name=None, event_output=False):
        self.id = id
        self.pin_id = pin_id
        self.name = name
        self.event_output = event_output

    def fill(self, query_result):
        self.id = query_result[0]
        self.pin_id = query_result[1]
        self.name = query_result[2]
        self.event_output = query_result[3] == 1

    @staticmethod
    def load():
        logger.debug(logger_name="Event", msg="Loading events")
        Event.__EVENTS.clear()
        data_source = DataSource.get_instance()
        Event.__EVENTS = data_source.query_for_dictionary(Event, Event.__ALL)
        logger.info(logger_name="Event", msg="Events loaded: " + str(len(Event.__EVENTS)))

    @staticmethod
    def get_event(event_id):
        if len(Event.__EVENTS) == 0:
            Event.load()
        return Event.__EVENTS[event_id]


class Task(Domain):
    __TASKS = {}
    __TASK_LIST = []
    __ALL = "select api_task.id, api_task.name, api_task.execution_time, api_task.execution_days, " \
            "api_task_events.event_id  from api_task, api_task_events " \
            "where api_task_events.task_id = api_task.id"
    __DETAIL = __ALL + " AND api_task.id = %s"

    def __init__(self, id=None, name=None, execution_time=None, execution_days="", events_id=[]):
        self.id = id
        self.name = name
        if execution_time is not None:
            self.execution_time = datetime.strptime(execution_time, "%H:%M:%S").time()
        self.execution_days = execution_days
        self.events_id = set(events_id)

    def execute_tasks(self):
        logger.info(logger_name="Task", msg="Executing task: " + self.name)
        logger.debug(logger_name="Task", msg="Events to execute: " + str(self.events_id))
        for event_id in self.events_id:
            logger.debug(logger_name="Task", msg="Execution Event : " + str(event_id))
            event = Event.get_event(event_id)
            pin = Pin.get_pin(event.pin_id)
            if event.event_output:
                pin.turn_on()
            else:
                pin.turn_off()
        logger.debug("Task: " + self.name + " done")

    @staticmethod
    def load():
        Task.__TASKS.clear()
        del Task.__TASK_LIST[:]
        data_source = DataSource.get_instance()
        rows = data_source.get_rows(Task.__ALL)
        for row in rows:
            task_id = row[0]
            if task_id in Task.__TASKS:
                task = Task.__TASKS[task_id]
                task.events_id.add(row[4])
            else:
                task = Task(id=row[0], name=row[1], execution_time=str(row[2]), execution_days=row[3])
                task.events_id.add(row[4])
                Task.__TASKS[task.id] = task
                Task.__TASK_LIST.append(task)
        logger.info(logger_name="Task", msg="Task loaded: " + str(len(Task.__TASKS)))

    @staticmethod
    def get_task(task_id, update=False):
        if len(Task.__TASKS) == 0 or update:
            Task.load()
        return Task.__TASKS[task_id]

    @staticmethod
    def get_task_list():
        if len(Task.__TASKS) == 0:
            Task.load()
        return Task.__TASK_LIST
