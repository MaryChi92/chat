import json

from log.deco_log_config import Log


class Utils:
    @staticmethod
    @Log()
    def get_message(sock):
        response = sock.recv(2048).decode('utf-8')
        return json.loads(response)

    @staticmethod
    @Log()
    def send_message(sock, message, uppercase=False):
        message = json.dumps(message).encode('utf-8')
        if uppercase:
            sock.send(message.upper())
        else:
            sock.send(message)
