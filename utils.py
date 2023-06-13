import json

from log.deco_log_config import Log


class Utils:
    @staticmethod
    @Log()
    def get_message(socket):
        response = socket.recv(2048).decode('utf-8')
        return json.loads(response)

    @staticmethod
    @Log()
    def send_message(socket, message, uppercase=False):
        message = json.dumps(message).encode('utf-8')
        if uppercase:
            socket.send(message.upper())
        else:
            socket.send(message)
