import unittest
from batch.domain import Pin, Event, Task
from batch.dateutils import cast_time_to_datetime, get_difference_in_seconds
from datetime import datetime
from batch.workers import TaskManager
from batch.dao import DataSource

DataSource.set_sql_type("sqLite")


class PinTest(unittest.TestCase):

    def get_pin_test(self):
        pin = Pin.get_pin(1)
        self.assertIsNotNone(pin)
        self.assertEqual(1, pin.id)

    def turn_off_pin_test(self):
        pin = Pin.get_pin(1)
        pin.turn_off()
        pin1 = Pin.get_pin(1)
        self.assertFalse(pin1.output)

    def turn_on_pin_test(self):
        pin = Pin.get_pin(1)
        pin.turn_on()
        pin1 = Pin.get_pin(1)
        self.assertTrue(pin1.output)

    def load_pins_test(self):
        pins = Pin.load()
        self.assertTrue(len(pins) > 0)
        pin = pins[0]
        self.assertIsNotNone(pin.pin_number)


class EventTest(unittest.TestCase):

    def get_event_test(self):
        event = Event.get_event(1)
        self.assertIsNotNone(event)
        self.assertEqual(1, event.id)
        self.assertIsNotNone(event.pin)

    def load_events_test(self):
        events = Event.load()
        self.assertTrue(len(events) > 0)
        self.assertIsNotNone(events[0])


class TaskTest(unittest.TestCase):

    def get_task_test(self):
        task = Task.get_task(1)
        self.assertIsNotNone(task)
        self.assertEqual(1, task.id)
        self.assertTrue(len(task.events) > 0)
        self.assertIsNotNone(task.events[0])

    def load_tasks_test(self):
        tasks = Task.load()
        self.assertTrue(len(tasks) > 0)
        self.assertIsNotNone(tasks[0])

    def execute_task_test(self):
        task = Task.get_task(1)
        task.execute_tasks()
        for event in task.events:
            self.assertEqual(event.event_output, event.pin.output)


class DateUtilsTest(unittest.TestCase):

    def cast_to_datetime_test(self):
        test_time = datetime.strptime("12:00:00", "%H:%M:%S").time()
        test_datetime = cast_time_to_datetime(test_time)
        self.assertTrue(test_datetime.date() is not None)

    def get_difference_in_seconds_test(self):
        datetime1 = datetime.strptime("12:00:00", "%H:%M:%S")
        datetime2 = datetime.strptime("11:59:00", "%H:%M:%S")
        seconds = get_difference_in_seconds(datetime1, datetime2)
        self.assertEqual(60, seconds)

        datetime1 = datetime.strptime("12:00:00", "%H:%M:%S")
        datetime2 = datetime.strptime("11:00:00", "%H:%M:%S")
        seconds = get_difference_in_seconds(datetime1, datetime2)
        self.assertEqual(3600, seconds)

        datetime1 = datetime.strptime("11:00:00", "%H:%M:%S")
        datetime2 = datetime.strptime("12:00:00", "%H:%M:%S")
        seconds = get_difference_in_seconds(datetime1, datetime2)
        self.assertEqual(-3600, seconds)


class ManagerTest(unittest.TestCase):

    def prepare_tasks_test(self):
        tasks = Task.load()
        awaiting_tasks = 0
        for task in tasks:
            if ManagerTest.__task_should_be_waiting(task):
                awaiting_tasks += 1
        TaskManager.start_tasks()
        self.assertEqual(awaiting_tasks, len(TaskManager.QUEUED_TIMER_TASKS))
        self.assertIsNotNone(TaskManager.MAIN_TIMER)
        for key, timer in TaskManager.QUEUED_TIMER_TASKS.iteritems():
            timer.cancel()
        TaskManager.MAIN_TIMER.cancel()

    @staticmethod
    def __task_should_be_waiting(task):
        today_datetime = datetime.now()
        task_datetime = cast_time_to_datetime(task.execution_time)
        day = datetime.today().weekday() + 1
        if str(day) in task.execution_days and get_difference_in_seconds(task_datetime, today_datetime) > 0:
            return True
        return False

if __name__ == '__main__':
    unittest.main()
