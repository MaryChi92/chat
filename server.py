import sys
from socket import AF_INET, SOCK_STREAM, socket
from select import select
from argparse import ArgumentParser
from collections import deque

from app.config import DEFAULT_PORT, DEFAULT_HOST, MAX_CONNECTIONS, TIMEOUT
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


def parse_params():
    parser = ArgumentParser()
    parser.add_argument('-p', type=int, default=DEFAULT_PORT, help='TCP-port')
    parser.add_argument('-a', default=DEFAULT_HOST, type=str, help='IP-address')
    namespace = parser.parse_args(sys.argv[1:])
    p_host = namespace.a
    p_port = namespace.p
    logger.info(
        f"IP-address: {p_host if p_host else DEFAULT_PORT}, TCP-port: {p_port if p_port else DEFAULT_HOST}"
    )
    return p_host, p_port


class Server(Utils, ProcessClientMessageMixin, metaclass=ServerVerifier):
    port = Port()

    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.users = Users()
        self.messages = deque()

        self.db = db

    # @staticmethod
    # @Log()
    # def parse_params():
    #     parser = ArgumentParser()
    #     parser.add_argument('-p', type=int, default=DEFAULT_PORT, help='TCP-port')
    #     parser.add_argument('-a', default=DEFAULT_HOST, type=str, help='IP-address')
    #     args = parser.parse_args()
    #     logger.info(
    #         f"IP-address: {args.a if args.a else DEFAULT_PORT}, TCP-port: {args.p if args.p else DEFAULT_HOST}"
    #     )
    #     return args.a, args.p

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
                if message["action"] == "presence":
                    if current_client_name not in self.users.usernames_sockets.keys():
                        self.users.usernames_sockets[current_client_name] = sock
                        client_ip, client_port = sock.getpeername()
                        self.db.client_login(current_client_name, client_ip, client_port)
                        # status_code_message = self.get_status_code_message(message)
                        response_message = self.make_message_template("login", alert="ok")
                        self.send_message(sock, response_message)
                        logger.info(f'Response message was sent: {response_message}')
                    else:
                        # status_code_message = self.get_status_code_message(message, status='error', error='User
                        # with this username already exists')
                        response_message = self.make_message_template("login", alert="error")
                        self.send_message(sock, response_message)
                        logger.info(f'Response message was sent: {response_message}')
                        self.users.delete_user(sock)
                        sock.close()
                    return
                elif message["action"] == "msg":
                    self.messages.append(message)
                    return
                elif message["action"] == "quit":
                    self.users.delete_user(sock, disconnect=True)
                    self.db.client_logout(current_client_name)
                    return
                else:
                    response_message = self.get_status_code_message('error', error='Incorrect request')
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

    c_host, c_port = parse_params()
    server = Server(c_host, c_port)
    server.run()
