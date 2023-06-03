import json


class Utils:
    @staticmethod
    def get_message(socket):
        response = socket.recv(2048).decode('utf-8')
        return json.loads(response)

    @staticmethod
    def send_message(socket, message):
        message = json.dumps(message).encode('utf-8')
        socket.send(message)
