from batch.dao import DataSource
from datetime import datetime
from utils import logger, raspberry


class Domain:

    def __init__(self):
        pass

    def fill(self, *query_result):
        pass


class Pin(Domain):
    __ALL = "SELECT id, pin_number, output, type FROM api_pin"
    __DETAIL = __ALL + " WHERE id = %s"
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
    def load():
        data_source = DataSource.get_instance()
        return data_source.query_for_list(domain_type=Pin, query=Pin.__ALL)

    @staticmethod
    def get_pin(pin_id):
        data_source = DataSource.get_instance()
        pin = data_source.query_for_object(Pin, Pin.__DETAIL, pin_id)
        return pin


class Event(Domain):
    __ALL = "SELECT id, pin_id, name, event_output FROM api_event"
    __DETAIL = __ALL + " WHERE id = %s"
    __EVENTS_BY_TASK = "SELECT api_event.id, pin_id, name, event_output from api_event, api_task_events" \
                   " WHERE api_event.id = api_task_events.event_id and api_task_events.task_id = %s"

    def __init__(self, id=None, pin_id=None, name=None, event_output=False):
        self.id = id
        if pin_id is not None:
            self.pin = Pin.get_pin(pin_id)
        self.name = name
        self.event_output = event_output

    def fill(self, query_result):
        self.id = query_result[0]
        self.pin = Pin.get_pin(query_result[1])
        self.name = query_result[2]
        self.event_output = query_result[3] == 1

    @staticmethod
    def load():
        data_source = DataSource.get_instance()
        return data_source.query_for_list(Event, Event.__ALL)

    @staticmethod
    def get_event(event_id):
        data_source = DataSource.get_instance()
        return data_source.query_for_object(Event, Event.__DETAIL, event_id)

    @staticmethod
    def get_events_by_task(task_id):
        data_source = DataSource.get_instance()
        return data_source.query_for_list(Event, Event.__EVENTS_BY_TASK, task_id)


class Task(Domain):
    __ALL = "select id, name, execution_time, execution_days from api_task"
    __DETAIL = __ALL + " where id = %s"

    def __init__(self, id=None, name=None, execution_time=None, execution_days="",):
        self.id = id
        self.name = name
        if execution_time is not None:
            self.execution_time = datetime.strptime(str(execution_time), "%H:%M:%S").time()
        self.execution_days = execution_days
        self.events = Event.get_events_by_task(self.id)

    def fill(self, query_result):
        self.id = query_result[0]
        self.name = query_result[1]
        self.execution_time = datetime.strptime(str(query_result[2]), "%H:%M:%S").time()
        self.execution_days = query_result[3]
        self.events = Event.get_events_by_task(self.id)

    def execute_tasks(self):
        logger.info(logger_name="Task", msg="Executing task: " + self.name)
        for event in self.events:
            logger.debug(logger_name="Task", msg="Execution Event : " + str(event.name))
            if event.event_output:
                event.pin.turn_on()
            else:
                event.pin.turn_off()
        logger.debug(logger_name="Task", msg="Task: " + self.name + " done")

    @staticmethod
    def load():
        data_source = DataSource.get_instance()
        return data_source.query_for_list(Task, Task.__ALL)

    @staticmethod
    def get_task(task_id):
        data_source = DataSource.get_instance()
        task = data_source.query_for_object(Task, Task.__DETAIL, task_id)
        return task

