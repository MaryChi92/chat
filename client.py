import sys
import time
from socket import AF_INET, SOCK_STREAM, socket
from argparse import ArgumentParser

from utils import Utils
from log.client_log_config import logger
from log.deco_log_config import Log


class Client(Utils):

    @staticmethod
    @Log()
    def create_message(action, **kwargs):
        message = {
            "action": action,
            "time": time.time(),
        }
        for k, v in kwargs.items():
            message[k] = v
        return message

    @staticmethod
    @Log()
    def parse_params():
        parser = ArgumentParser()
        parser.add_argument('a', type=str, default='localhost', help='IP-address')
        parser.add_argument('p', type=int, default=7777, help='TCP-port')
        parser.add_argument('-m', type=str, default='listen', help='Mode: send or listen')
        args = parser.parse_args()
        logger.info(
            f"IP-address: {args.a if args.a else 7777}, TCP-port: {args.p if args.p else 'localhost'}"
        )
        return args.a, args.p, args.m

    @Log()
    def connect_to_socket(self, addr, port):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((addr, port))
        logger.info(f'Connected to server: {port}:{addr}')
        return sock

    @Log()
    def main(self):
        addr, port, mode = self.parse_params()
        try:
            sock = self.connect_to_socket(addr, port)
            presence_message = self.create_message(action="presence", type="status",
                                                   user={"account_name": "kiki159", "status": "Online!"}
                                                   )
            self.send_message(sock, presence_message)
            response = self.get_message(sock)
            logger.info(f'The response from the server was received: {response}')
        except Exception as e:
            logger.error(f'Something went wrong: {e}')
            sys.exit(1)
        else:
            if mode == 'listen':
                print('Ready to get messages')
            elif mode == 'send':
                print('Ready to send messages')

            while True:
                if mode == 'listen':
                    try:
                        message = self.get_message(sock)
                    except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                        logger.error(f'Connection with the server {addr} was lost')
                        sys.exit(1)
                    else:
                        logger.info(f'The message was received: {message}')

                if mode == 'send':
                    while message := input("Enter your message or Q for exit: ") != 'Q':
                        _message = self.create_message(action="message", body=message)
                        self.send_message(sock, _message)
                        logger.info(f'Message {_message} was sent')


if __name__ == '__main__':
    client = Client()
    client.main()
