import sys
import time
from socket import AF_INET, SOCK_STREAM, socket
from argparse import ArgumentParser

from utils import Utils


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
        return args.a, args.p

    def main(self):
        try:
            s = socket(AF_INET, SOCK_STREAM)
            s.connect(self.parse_params())
        except Exception as e:
            print(e)
            sys.exit(1)

        self.send_message(s, self.presence_message)

        response = self.get_message(s)
        print(response)


if __name__ == '__main__':
    client = Client()
    client.main()
