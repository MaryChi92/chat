import sys
from socket import AF_INET, SOCK_STREAM, socket
from argparse import ArgumentParser

from utils import get_message, send_message


resp_code_200 = {
    "response": 200,
    "alert": "Подключение прошло успешно"
}

resp_code_400 = {
    "response": 200,
    "alert": "Ошибка при подключении"
}


def parse_params():
    parser = ArgumentParser()
    parser.add_argument('-p', type=int, default=7777, help='TCP-port')
    parser.add_argument('-a', default='localhost', type=str, help='IP-address')
    args = parser.parse_args()
    return args.a, args.p


def main():
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.bind(parse_params())
        s.listen(3)
    except Exception as e:
        print(e)
        sys.exit(1)

    while True:
        client, addr = s.accept()
        message = get_message(client)

        if 'action' in message and 'time' in message:
            print(message)
            send_message(client, resp_code_200)
        else:
            send_message(client, resp_code_400)

        client.close()


if __name__ == '__main__':
    main()
