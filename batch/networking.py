import socket
import sys
import time

from utils import logger


class Server:
    __HOST = ''
    __PORT = 10000

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logger.debug(logger_name="Socket_Server", msg="Created Socket")
        try:
            self.socket.bind((Server.__HOST, Server.__PORT))
            logger.debug(logger_name="Socket_Server", msg="Socket server bind")
            self.socket.listen(10)
            logger.debug(logger_name="Socket_Server", msg="Starting listener")
        except socket.error as msg:
            logger.error(logger_name="Socket_Server", msg=('Error Code : ' + str(msg[0]) + ' Message ' + msg[1]))
            sys.exit()

    def start(self):
        while 1:
            logger.debug(logger_name="Socket_Server", msg="Waiting for client")
            conn, addr = self.socket.accept()
            logger.info(logger_name="Socket_Server", msg=('Connected with ' + addr[0] + ':' + str(addr[1])))
            try:
                while True:
                    data = conn.recv(16)
                    if data:
                        message = Message(data=data)
                        self.__process_data(conn=conn, message=message)
                    else:
                        break
            except socket.error as msg:
                logger.error(logger_name="Socket_Server", msg=('Error Code : ' + str(msg[0]) + ' Message ' + msg[1]))

    def __process_data(self, conn, message=None):
        logger.debug(logger_name="Socket_Server", msg=('received ' + str(message)))
        conn.sendall(str(message))

    def close(self):
        self.socket.close()


class Client:
    __HOST = ''
    __PORT = 10000

    def __init__(self):
        self.socket = None

    def start(self, attempts=1):
        attempts_done = 0
        connected = False
        while attempts_done <= attempts:
            logger.debug(logger_name="Socket_Client",
                        msg=('Connection attempt ' + str(attempts_done) + ' of ' + str(attempts)))
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                logger.debug(logger_name="Socket_Client", msg="Created Socket")
                self.socket.connect((Client.__HOST, Client.__PORT))
                logger.info(logger_name="Socket_Client",
                            msg=("Socket connected to " + Client.__HOST + ":" + str(Client.__PORT)))
                connected = True
                break
            except socket.error as msg:
                logger.error(logger_name="Socket_Client", msg=('Error Code : ' + str(msg[0]) + ' Message ' + msg[1]))
            time.sleep(5)
            attempts_done += 1
        if connected is False:
            sys.exit()

    def send_message(self, message=None):
        if message is None:
            raise Exception("message can't be None")
        try:
            logger.info(logger_name="Socket_Client", msg=("Sending message: " + message))
            self.socket.sendall(message)
            amount_received = 0
            amount_expected = len(message)
            while amount_received < amount_expected:
                data = self.socket.recv(16)
                amount_received += len(data)
                logger.info(logger_name="Socket_Client", msg=("Message received: " + message))
        finally:
            self.socket.close()


class Message:

    def __init__(self, element="", event="", id="", data=None):
        if data is not None:
            data = data.replace("{", "").replace("}","")
            parts = data.split(",")
            for part in parts:
                tupla = part.split(":")
                if tupla[0] == "element":
                    self.element = tupla[1]
                elif tupla[0] == "event":
                    self.event = tupla[1]
                elif tupla[0] == "id":
                    self.id = tupla[1]
        else:
            self.element = element
            self.event = event
            self.id = id

    def __str__(self):
        return "{element:" + self.element + ",event:" + self.event + ",id:" + self.id + "}"
