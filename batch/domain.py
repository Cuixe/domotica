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
    __DETAIL = __ALL + " WHERE id=%s"
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
        logger.debug(logger_name="Pin", msg=("Pin: " + str(self.pin_number) + " turned on"))

    def turn_off(self):
        self.output = False
        raspberry.call_pin(self.pin_number, self.output)
        self.__update()
        logger.debug(logger_name="Pin", msg=("Pin: " + str(self.pin_number) + " turned off"))

    def fill(self, query_result):
        self.id = query_result[0]
        self.pin_number = query_result[1]
        self.output = query_result[2] == 1
        self.type = query_result[3]

    def __update(self):
        data_source = DataSource.get_instance()
        data_source.execute(Pin.__UPDATE, [1 if self.output else 0, self.id])

    @staticmethod
    def load(execute=False):
        logger.debug(logger_name="Pin", msg="Loading pins")
        Pin.__PINS.clear()
        data_source = DataSource.get_instance()
        Pin.__PINS = data_source.query_for_dictionary(domain_type=Pin, query=Pin.__ALL)
        logger.info(logger_name="Pin", msg="Pins loaded: " + str(len(Pin.__PINS)))
        if execute:
            for key, pin in Pin.__PINS.iteritems():
                if pin.output:
                    pin.turn_on()
                else:
                    pin.turn_off()

    @staticmethod
    def get_pin(pin_id, update=False):
        logger.debug(logger_name="Pin", msg="Pin requested " + str(pin_id))
        if pin_id not in Pin.__PINS or update is True:
            data_source = DataSource.get_instance()
            pin = data_source.query_for_object(Pin, Pin.__DETAIL, pin_id)
            Pin.__PINS[pin.id] = pin
        return Pin.__PINS[pin_id]


class Event(Domain):
    __EVENTS = {}
    __ALL = "SELECT id, pin_id, name, event_output FROM api_event"
    __DETAIL = __ALL + " WHERE id = %s"
    __EVENTS_BY_TASK = "SELECT id, pin_id, name, event_output FROM api_event where id in"\
                       " (SELECT event_id FROM api_task_events where task_id = %s)"

    def __init__(self, id=None, pin_id=None, name=None, event_output=False):
        self.id = id
        if pin_id is not None:
            self.pin = Pin.get_pin(pin_id=pin_id)
        self.name = name
        self.event_output = event_output

    def fill(self, query_result):
        self.id = query_result[0]
        self.name = query_result[2]
        self.event_output = query_result[3] == 1
        self.pin = Pin.get_pin(pin_id=query_result[1])

    @staticmethod
    def load():
        logger.debug(logger_name="Event", msg="Loading events")
        Event.__EVENTS.clear()
        data_source = DataSource.get_instance()
        Event.__EVENTS = data_source.query_for_dictionary(Event, Event.__ALL)
        logger.info(logger_name="Event", msg="Events loaded: " + str(len(Event.__EVENTS)))

    @staticmethod
    def get_event(event_id, update=False):
        if event_id not in Event.__EVENTS or update:
            data_source = DataSource.get_instance()
            event = data_source.query_for_object(Event, Event.__DETAIL, event_id)
            Event.__EVENTS[event.id] = event
        return Event.__EVENTS[event_id]

    @staticmethod
    def get_events_by_task(task_id):
        data_source = DataSource.get_instance()
        return data_source.query_for_list(Event, Event.__EVENTS_BY_TASK, task_id)


class Task(Domain):
    __TASKS = {}
    __ALL = "select id, name, execution_time, execution_days from api_task where enabled = 1"
    __DETAIL = __ALL + " AND api_task.id = %s"

    def __init__(self, id=None, name=None, execution_time=None, execution_days=""):
        self.id = id
        self.name = name
        if execution_time is not None:
            self.execution_time = datetime.strptime(execution_time, "%H:%M:%S").time()
        self.execution_days = execution_days
        self.events = Event.get_events_by_task(id)

    def fill(self, query_result):
        self.id = query_result[0]
        self.name = query_result[1]
        self.execution_time = query_result[2]
        self.execution_days = query_result[3]
        self.events = Event.get_events_by_task(self.id)

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
        data_source = DataSource.get_instance()
        Task.__TASKS = data_source.query_for_dictionary(Task, Task.__ALL)
        logger.info(logger_name="Task", msg="Task loaded: " + str(len(Task.__TASKS)))
        return Task.__TASKS

    @staticmethod
    def get_task(task_id, update=False):
        if task_id not in Task.__TASKS or update:
            data_source = DataSource.get_instance()
            task = data_source.query_for_object(Task, Task.__DETAIL, task_id)
            Task.__TASKS[task.id] = task
        return Task.__TASKS[task_id]
