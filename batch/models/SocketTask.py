import datetime
from batch.dao.DataSource import DataSource
from batch.models.Socket import Socket


class SocketTask(object):
    dataSource = DataSource()
    __UPDATE = "UPDATE api_socket SET owner_id=?, name=?, number=?, rapsPin=?, status=? where id=?"
    __ALL="SELECT id, socket_id, executionTime, newStatus, frequency FROM api_socketworker"
    sockets_task = None

    def __init__(self, id=0, socket_id=1, execution_time=datetime.time, new_status=False, frequency=""):
        self.id = id
        self.socket = Socket.get_socket(socket_id)
        self.execution_time = datetime.datetime.strptime(execution_time, "%H:%M:%S").time()
        self.new_status = new_status
        self.frequency = frequency

    def __str__(self):
        return "{'id':'" + str(self.id) + "','socket_id':'" + str(
            self.socket.id) + "','execution_time':'" + str(self.execution_time) + "', 'new_status':'" + str(
            self.new_status) + ", 'frequency':'" + str(self.frequency) + "'}"

    @staticmethod
    def get_socket_tasks():
        if SocketTask.sockets_task is None:
            SocketTask.reload_socket_tasks()
        return SocketTask.sockets_task

    @staticmethod
    def reload_socket_tasks():
        SocketTask.sockets_task = []
        rows = SocketTask.dataSource.get_rows(query=SocketTask.__ALL)
        for row in rows:
            task = SocketTask(id=row[0], socket_id=row[1], execution_time=row[2], new_status=row[3],
                                frequency=row[4])
            SocketTask.sockets_task.append(task)