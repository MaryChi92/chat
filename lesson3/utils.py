import json


def get_message(s):
    response = s.recv(2048).decode('utf-8')
    return json.loads(response)


def send_message(s, message):
    message = json.dumps(message).encode('utf-8')
    s.send(message)
