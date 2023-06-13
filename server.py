import sys
from socket import AF_INET, SOCK_STREAM, socket
from select import select
from argparse import ArgumentParser
from collections import deque

from utils import Utils
from log.server_log_config import logger
from log.deco_log_config import Log


class Server(Utils):
    def __init__(self):
        self.clients = []
        self.messages = deque()

    @staticmethod
    @Log()
    def get_response_message(message):
        logger.info(f"Getting a response for client's message {message}")

        resp_code_200 = {
            "response": 200,
            "alert": "Successfully connected"
        }
        resp_code_400 = {
            "response": 400,
            "alert": "Error"
        }

        if 'action' in message and 'time' in message:
            return resp_code_200
        return resp_code_400

    @staticmethod
    @Log()
    def parse_params():
        parser = ArgumentParser()
        parser.add_argument('-p', type=int, default=7777, help='TCP-port')
        parser.add_argument('-a', default='localhost', type=str, help='IP-address')
        args = parser.parse_args()
        logger.info(
            f"IP-address: {args.a if args.a else 7777}, TCP-port: {args.p if args.p else 'localhost'}"
        )
        return args.a, args.p

    @Log()
    def init_socket(self):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind(self.parse_params())
        sock.settimeout(0.5)
        sock.listen(5)
        logger.info(f'Socket was successfully created')
        return sock

    @Log()
    def check_requests(self, recv_data_clients_list, all_clients):
        for sock in recv_data_clients_list:
            try:
                message = self.get_message(sock)
                self.messages.append(message)
            except:
                logger.info(f'Client {sock.getpeername()} disconnected')
                all_clients.remove(sock)

    @Log()
    def write_responses(self, send_data_clients_list, all_clients):
        while self.messages:
            message = self.messages.popleft()
            for sock in send_data_clients_list:
                    try:
                        self.send_message(sock, message, uppercase=True)
                    except:
                        logger.info(f'Client {sock.getpeername()} disconnected')
                        sock.close()
                        all_clients.remove(sock)

    @Log()
    def main(self):
        try:
            sock = self.init_socket()
        except Exception as e:
            logger.error(f'Something went wrong: {e}')
            sys.exit(1)

        while True:
            try:
                client, addr = sock.accept()
            except OSError:
                pass
            else:
                logger.info(f'The connection was set - client: {client}, address: {addr}')
                self.clients.append(client)
            finally:
                recv_data_clients_list = []
                send_data_clients_list = []
                err_list = []

                try:
                    if self.clients:
                        recv_data_clients_list, send_data_clients_list, err_list = select(self.clients,
                                                                                          self.clients, [], 0)
                except OSError:
                    pass

                if recv_data_clients_list:
                    self.check_requests(recv_data_clients_list, self.clients)
                    if self.messages and send_data_clients_list:
                        self.write_responses(send_data_clients_list, self.clients)


if __name__ == '__main__':
    server = Server()
    server.main()
