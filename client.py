import sys
import time
from socket import AF_INET, SOCK_STREAM, socket
from argparse import ArgumentParser

from utils import Utils
from log.client_log_config import logger


class Client(Utils):
    presence_message = {
        "action": "presence",
        "time": time.time(),
        "type": "status",
        "user": {
            "account_name": "kiki159",
            "status": "Online!"
        }
    }

    @staticmethod
    def parse_params():
        parser = ArgumentParser()
        parser.add_argument('a', type=str, default='localhost', help='IP-address')
        parser.add_argument('p', type=int, default=7777, help='TCP-port')
        args = parser.parse_args()
        logger.info(
            f"IP-address: {args.a if args.a else 7777}, TCP-port: {args.p if args.p else 'localhost'}"
        )
        return args.a, args.p

    def main(self):
        try:
            s = socket(AF_INET, SOCK_STREAM)
            addr, sock = self.parse_params()
            s.connect((addr, sock))
            logger.info(f'Connected to server: {sock}:{addr}')
        except Exception as e:
            logger.error(f'Something went wrong: {e}')
            sys.exit(1)

        self.send_message(s, self.presence_message)
        logger.info(f'The presence message ({self.presence_message}) was sent to the server: {sock}:{addr}')

        response = self.get_message(s)
        logger.info(f'The response from the server was received: {response}')


if __name__ == '__main__':
    client = Client()
    client.main()
