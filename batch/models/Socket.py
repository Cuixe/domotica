from batch.dao.DataSource import DataSource
from raspberry.operations import operation


class Socket(object):
    dataSource = DataSource()
    __UPDATE = "UPDATE api_socket SET owner_id=?, name=?, number=?, rapsPin=?, status=? where id=?"
    __ALL = "SELECT id, owner_id, name, number, rapsPin, status FROM api_socket"
    sockets = None

    def __init__(self, id=0, owner_id=1, name="", number=0, rasp_pin=0, status=False):
        self.id = id
        self.owner_id = owner_id
        self.name = name
        self.number = number
        self.rasp_pin = rasp_pin
        self.status = status

    def __str__(self):
        return "{'id':'" + str(self.id) + "','owner_id':'" + str(
            self.owner_id) + "','name':'" + self.name + "', 'number':'" + str(self.number) + ", 'pin':'" + str(
            self.rasp_pin) + ",' status':'" + str(self.status) + "'}"

    def turn_on(self):
        self.status = True
        self.update()
        operation(self.rasp_pin, False)

    def turn_off(self):
        self.status = False
        self.update()
        operation(self.rasp_pin, False)

    def update(self):
        Socket.dataSource.execute(Socket.__UPDATE, self.owner_id, self.name, self.number, self.rasp_pin, self.status,
                                  self.id)

    @staticmethod
    def get_sockets():
        if Socket.sockets is None:
            Socket.reload_sockets()
        return Socket.sockets

    @staticmethod
    def reload_sockets():
        Socket.sockets = []
        rows = Socket.dataSource.get_rows(query=Socket.__ALL)
        for row in rows:
            socket = Socket(id=row[0], owner_id=row[1], name=row[2], number=row[3],
                            rasp_pin=row[4], status=(row[5] == 1))
            Socket.sockets.append(socket)

    @staticmethod
    def get_socket(socket_id=0):
        if Socket.sockets is None:
            Socket.reload_sockets()
        for socket in Socket.sockets:
            if socket.id == socket_id:
                return socket
