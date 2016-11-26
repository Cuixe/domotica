from batch.workers import Manager
import datetime
import time

"""
sockets = Socket.get_sockets()
for socket in sockets:
    print socket

socket.turn_off()
print 'Nuevos valores:'
sockets = Socket.get_sockets()
for socket in sockets:
    print socket


tasks = SocketTask.get_socket_tasks()
for task in tasks:
    print task
"""
date = datetime.datetime(year=2016, month=11, day=21)
print datetime.datetime.today().weekday()
now = datetime.datetime.now().time()

task = SocketTask(execution_time="23:59:59")
FMT = "%H:%M:%S"
execution_time = (task.execution_time.hour * 3600) + (task.execution_time.minute) * 60 + task.execution_time.second
now_time = (now.hour * 3600) + (now.minute * 60) + now.second
print execution_time - now_time

fecha = str(datetime.datetime.now().date()) + " " + str(task.execution_time)
print fecha
exect = datetime.datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
print exect
abc = exect - datetime.datetime.now()
print abc.total_seconds()


def wait_for_end(manager):
    for task in manager.queued_tasks.values():
        if task.finished.is_set() == False:
            time.sleep(1)
            wait_for_end(manager)


manager = Manager()
manager.run()
wait_for_end(manager)


