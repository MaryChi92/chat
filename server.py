import sys
from socket import AF_INET, SOCK_STREAM, socket
from select import select
from collections import deque
from http import HTTPStatus

from app.config import MAX_CONNECTIONS, TIMEOUT
from app.server_utils import parse_params
from app.utils import ProcessClientMessageMixin, Users, Utils
from log.server_log_config import logger
from log.deco_log_config import Log
from descriptor import Port
from metaclasses import BaseVerifier
from app.models import Storage


class ServerVerifier(BaseVerifier):
    def __init__(cls, name, bases, namespaces):
        super().__init__(name, bases, namespaces)

        if "connect" in cls.attrs[f"_{name}_attrs"]:
            raise TypeError("Connect method is not allowed")


class Server(Utils, ProcessClientMessageMixin, metaclass=ServerVerifier):
    port = Port()

    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.users = Users()
        self.messages = deque()

        self.db = db

    @Log()
    def init_socket(self):
        sock = socket(AF_INET, SOCK_STREAM)
        # address, self.port = self.parse_params
        sock.bind((self.host, self.port))
        sock.settimeout(TIMEOUT)
        sock.listen(MAX_CONNECTIONS)
        logger.info(f'Socket was successfully created')
        return sock

    @Log()
    def check_requests(self, recv_data_clients_list):
        for sock in recv_data_clients_list:
            try:
                message = self.get_message(sock)
                current_client_name = message["user"]["username"]
                logger.info(f'Received message from client {current_client_name}: {message}')

                # process presence message
                if message["action"] == "presence":
                    response_message = self.make_message_template(action='status code', response=HTTPStatus.OK,
                                                                  alert='ok')
                    self.send_message(sock, response_message)
                    logger.info(f'Response message was sent: {response_message}')

                elif message["action"] == "login":
                    if current_client_name not in self.users.usernames_sockets.keys():
                        self.users.usernames_sockets[current_client_name] = sock
                        client_ip, client_port = sock.getpeername()
                        self.db.client_login(current_client_name, client_ip, client_port)
                        response_message = self.make_message_template(action='login', result='accepted')
                        self.send_message(sock, response_message)
                        logger.info(f'Response message was sent: {response_message}')
                    else:
                        response_message = self.make_message_template(action='status code', result='rejected',
                                                                      error='Username already exists')
                        self.send_message(sock, response_message)
                        logger.info(f'Response message was sent: {response_message}')
                        self.users.delete_user(sock)
                        sock.close()
                    return

                # process sending message to another client
                elif message["action"] == "msg":
                    self.messages.append(message)
                    return

                # process quit message
                elif message["action"] == "quit":
                    self.db.client_logout(current_client_name)
                    self.users.delete_user(sock, disconnect=True)
                    return

                # process incorrect request
                else:
                    response_message = self.make_message_template(error='Incorrect request')
                    self.send_message(sock, response_message)
                    return

            except Exception as e:
                logger.error(f'Client {sock.getpeername()} disconnected, error {e}')
                self.users.sockets.remove(sock)

    @Log()
    def write_responses(self, send_data_clients_list):
        while self.messages:
            message = self.messages.popleft()
            destination_username = message["to_user"]
            if destination_username in self.users.usernames_sockets and \
                    self.users.usernames_sockets[destination_username] in send_data_clients_list:
                self.send_message(self.users.usernames_sockets[destination_username], message)
                logger.info(f'A message was sent to user {destination_username}'
                            f'from user {message["user"]["username"]}')
            elif destination_username in self.users.usernames_sockets and \
                    self.users.usernames_sockets[destination_username] not in send_data_clients_list:
                raise ConnectionError
            else:
                logger.error(f'User {destination_username} is not registered, message can not be sent')

    @Log()
    def run(self):
        try:
            self.sock = self.init_socket()
        except Exception as e:
            logger.error(f'Something went wrong: {e}')
            sys.exit(1)

        while True:
            try:
                client, addr = self.sock.accept()
            except OSError:
                pass
            else:
                logger.info(f'The connection was set - client: {client}, address: {addr}')
                self.users.sockets.append(client)
            finally:
                recv_data_clients_list = []
                send_data_clients_list = []
                err_list = []

                try:
                    if self.users.sockets:
                        recv_data_clients_list, send_data_clients_list, err_list = select(self.users.sockets,
                                                                                          self.users.sockets, [], 0)
                except OSError:
                    pass

                if recv_data_clients_list:
                    self.check_requests(recv_data_clients_list)
                    if self.messages and send_data_clients_list:
                        self.write_responses(send_data_clients_list)


if __name__ == '__main__':
    db = Storage()

    host, port = parse_params()
    server = Server(host, port)
    server.run()
