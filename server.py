import sys
from socket import AF_INET, SOCK_STREAM, socket
from argparse import ArgumentParser

from utils import Utils


class Server:

    @staticmethod
    def get_response_message(message):
        resp_code_200 = {
            "response": 200,
            "alert": "Подключение прошло успешно"
        }
        resp_code_400 = {
            "response": 400,
            "alert": "Ошибка при подключении"
        }

        if 'action' in message and 'time' in message:
            return resp_code_200
        return resp_code_400

    @staticmethod
    def parse_params():
        parser = ArgumentParser()
        parser.add_argument('-p', type=int, default=7777, help='TCP-port')
        parser.add_argument('-a', default='localhost', type=str, help='IP-address')
        args = parser.parse_args()
        return args.a, args.p

    def main(self):
        try:
            s = socket(AF_INET, SOCK_STREAM)
            s.bind(self.parse_params())
            s.listen(3)
        except Exception as e:
            print(e)
            sys.exit(1)

        while True:
            client, addr = s.accept()
            message = Utils.get_message(client)
            print(message)

            response = self.get_response_message(message)
            Utils.send_message(client, response)

            client.close()


if __name__ == '__main__':
    server = Server()
    server.main()
