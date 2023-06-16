import sys
import threading
import time
from socket import AF_INET, SOCK_STREAM, socket
from argparse import ArgumentParser
from threading import Thread

from app.config import DEFAULT_PORT, DEFAULT_HOST, TIMEOUT
from app.utils import Utils
from log.client_log_config import logger
from log.deco_log_config import Log


class Client(Utils):
    def __init__(self):
        self.username = None

    @Log()
    def create_message(self, action, **kwargs):
        user = {"username": self.username, "status": "online"}
        logger.info(f'Creating message from user: {user["username"]}')
        return self.make_message_template(action=action, user=user, **kwargs)

    @staticmethod
    @Log()
    def parse_params():
        parser = ArgumentParser()
        parser.add_argument('a', type=str, default=DEFAULT_HOST, help='IP-address')
        parser.add_argument('p', type=int, default=DEFAULT_PORT, help='TCP-port')
        args = parser.parse_args()
        logger.info(
            f"IP-address: {args.a if args.a else DEFAULT_PORT}, TCP-port: {args.p if args.p else DEFAULT_HOST}"
        )
        return args.a, args.p

    @Log()
    def parse_message(self, message):
        logger.info(f'Parsing message from the server: {message}')

        if message["action"] == "login":
            if message["alert"] == "ok":
                return f'You are logged in'
            return 'Rejected'

        if message["action"] == "msg" and message["to_user"] == self.username:
            return f'{message["body"]}'

    @Log()
    def connect_to_socket(self, addr, port):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((addr, port))
        logger.info(f'Connected to server: {port}:{addr}')
        return sock

    @Log()
    def set_username(self):
        while not self.username:
            self.username = input('Enter your name: ')
            presence_message = self.create_message(action="presence", type="status")
            self.send_message(self.sock, presence_message)
            response = self.get_message(self.sock)
            logger.info(f'The response from the server was received: {response}')
            parsed_message = self.parse_message(response)
            if parsed_message == 'Rejected':
                print(f'{parsed_message}')
                self.username = None

    @Log()
    def get_and_parse_message(self):
        try:
            message = self.get_message(self.sock)
        except Exception as e:
            logger.critical(f'Error while getting message: {e}')
            sys.exit(1)
        else:
            logger.info(f'The message was received: {message}')
            return self.parse_message(message)

    @Log()
    def incoming_stream(self):
        while message := self.get_and_parse_message():
            print(message)

    @Log()
    def outgoing_stream(self):
        while command := input('Enter "message" to send a message or "Q" to quit: '):
            if command == 'Q':
                break
            elif command == "message":
                message = input('Text your message here: ')
                addressee = input('Enter addressee(username): ')
                self.send_message(
                    self.sock,
                    self.create_message(
                        action="msg",
                        body=message,
                        to_user=addressee,
                    ),
                )

    @Log()
    def main(self):
        addr, port = self.parse_params()
        try:
            self.sock = self.connect_to_socket(addr, port)
            self.set_username()
        except Exception as e:
            logger.critical(f'Something went wrong: {e}')
            sys.exit(1)


if __name__ == '__main__':
    client = Client()
    client.main()
    client.set_username()

    receiver = Thread(target=client.incoming_stream)
    receiver.daemon = True
    receiver.start()

    transmitter = Thread(target=client.outgoing_stream)
    transmitter.daemon = True
    transmitter.start()

    while True:
        time.sleep(TIMEOUT)
        if receiver.is_alive() and transmitter.is_alive():
            continue
        break
