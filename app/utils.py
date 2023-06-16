import json
from time import time

from app.config import ENCODING, MAX_PACKAGE_LENGTH
from log.server_log_config import logger
from log.deco_log_config import Log


class Users:
    def __init__(self):
        self.sockets = []
        self.usernames_sockets = {}

    def get_username_by_sock(self, sock):
        for username, _sock in self.usernames_sockets:
            if _sock == sock:
                return username

    def delete_user(self, sock, disconnect=False):
        username = self.get_username_by_sock(sock)
        if disconnect:
            sock.close()
        if username:
            del self.usernames_sockets[username]
        self.sockets.remove(sock)


class ProcessClientMessageMixin:
    @staticmethod
    @Log()
    def get_status_code_message(message=False, status='ok', error='error'):
        if message:
            logger.info(f"Getting a response for client's presence message {message}")

        if status == 'ok':
            return f'resp_code = {"response": "200", "alert": "Ok"}'
        return f'resp_code = {"response": "400", "error": "{error}"}'

    def process_client_message(self, message, sock, users):
        pass


class Utils:
    @staticmethod
    @Log()
    def get_message(sock):
        response = sock.recv(MAX_PACKAGE_LENGTH).decode(ENCODING)
        return json.loads(response)

    @staticmethod
    @Log()
    def send_message(sock, message):
        message = json.dumps(message).encode(ENCODING)
        sock.send(message)

    @staticmethod
    def make_message_template(action, **kwargs):
        message = {
            "action": action,
            "time": time(),
        }
        for k, v in kwargs.items():
            message[k] = v
        return message
