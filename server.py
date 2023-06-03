import sys
from socket import AF_INET, SOCK_STREAM, socket
from argparse import ArgumentParser

from utils import Utils
from log.server_log_config import logger


class Server:

    @staticmethod
    def get_response_message(message):
        logger.info(f"Getting a response for client's message {message}")

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
        logger.info(
            f"IP-address: {args.a if args.a else 7777}, TCP-port: {args.p if args.p else 'localhost'}"
        )
        return args.a, args.p

    def main(self):
        try:
            s = socket(AF_INET, SOCK_STREAM)
            s.bind(self.parse_params())
            s.listen(3)
        except Exception as e:
            logger.error(f'Something went wrong: {e}')
            sys.exit(1)

        while True:
            client, addr = s.accept()
            logger.info(f'The connection was set - client: {client}, address: {addr}')
            message = Utils.get_message(client)
            logger.info(f'The message from client was received: {message}')

            response = self.get_response_message(message)
            logger.info(f'The response for the client was created: {response}')
            Utils.send_message(client, response)
            logger.info(f'The response ({response}) for the client ({client}) was sent')

            client.close()
            logger.info(f'The connection with client was closed - client: {client}, address - {addr}')


if __name__ == '__main__':
    server = Server()
    server.main()
