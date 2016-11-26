import unittest
from batch.domain import Pin, Event, Task
from batch.dateutils import cast_time_to_datetime, get_difference_in_seconds
from datetime import datetime, timedelta
from batch.workers import Manager
import time
import collections


class DomainTest(unittest.TestCase):

    def pin_test(self):
        Pin.load()
        pin = Pin.get_pin(1)
        self.assertIsNotNone(pin)

    def event_test(self):
        Event.load()
        event = Event.get_event(1)
        self.assertIsNotNone(event)

    def task_test(self):
        Task.load()
        task = Task.get_task(1)
        self.assertIsNotNone(task)
        self.assertTrue(len(task.events_id) == 3)

        task = Task.get_task(2)
        self.assertIsNotNone(task)
        self.assertTrue(len(task.events_id) == 1)


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

    def manager_test(self):
        index = 1
        pin = Pin.get_pin(index)
        while pin is not None:
            pin.output = (index % 2) is not 0
            index += 1
            try:
                pin = Pin.get_pin(index)
            except:
                pin = None
        tasks = Task.get_task_list()
        day = str(datetime.today().weekday() + 1)
        index = 2
        for task in tasks:
            date = datetime.now() + timedelta(seconds=index)
            task.execution_time = date.time()
            task.execution_days = day
            index += 2
        manager = Manager()
        manager.start_tasks()
        print datetime.now().strftime(" %H:%M:%S")
        for task in tasks:
            time.sleep(2)
            for event_id in task.events_id:
                event = Event.get_event(event_id)
                pin = Pin.get_pin(event.pin_id)
                self.assertEqual(event.event_output, pin.output,
                                 msg=task.name + ": " + str(event.event_output) + " != " + str(pin.output))

    def before_task_test(self):
        dictionary = {}
        dictionary[-7] = Task(name="4")
        dictionary[-7.5] = Task(name="2")
        dictionary[-7.49] = Task(name="3")
        dictionary[-4] = Task(name="6")
        dictionary[-7.51] = Task(name="1")
        dictionary[-5] = Task(name="5")
        dictionary = collections.OrderedDict(sorted(dictionary.items()))

        index = 1
        for key, task in dictionary.iteritems():
            self.assertEqual(str(index), task.name)
            print str(task.name)
            index += 1


if __name__ == '__main__':
    unittest.main()
