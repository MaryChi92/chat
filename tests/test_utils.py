import json
import unittest
import sys
import os
import time

sys.path.append(os.getcwd())
from app.utils import Utils


class TestSocket:
    def __init__(self, message):
        self.encoded_message = json.dumps(message).encode('utf-8')

    def send(self, message):
        self.sent_message = json.loads(message.decode('utf-8'))

    def recv(self, message):
        return self.encoded_message


class TestUtils(unittest.TestCase):
    def setUp(self) -> None:
        self.utils = Utils
        self.message = {'action': 'presence', 'time': time.time()}
        self.test_socket = TestSocket(self.message)

    def test_send_message(self):
        self.utils.send_message(self.test_socket, self.message)
        self.assertEqual(self.test_socket.sent_message, self.message)

    def test_get_message(self):
        message = self.utils.get_message(self.test_socket)
        self.assertEqual(message, self.message)


if __name__ == '__main__':
    unittest.main()
