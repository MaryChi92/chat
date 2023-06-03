import unittest
import sys
import os
import time
from unittest.mock import patch

sys.path.append(os.getcwd())
from server import Server


class TestServer(unittest.TestCase):

    TEST_ADDR = '127.0.0.1'
    TEST_PORT = 8080

    def setUp(self) -> None:
        self.server = Server
        self.time = time.time()


    def test_parse_params_no_params_passed(self):
        self.assertEqual(self.server.parse_params(), ('localhost', 7777))

    @patch('sys.argv', ['', '-a', TEST_ADDR])
    def test_parse_params_only_address_passed(self):
        self.assertEqual(self.server.parse_params(), ('127.0.0.1', 7777))

    @patch('sys.argv', ['', '-p', str(TEST_PORT)])
    def test_parse_params_only_port_passed(self):
        self.assertEqual(self.server.parse_params(), ('localhost', 8080))

    @patch('sys.argv', ['', '-a', TEST_ADDR, '-p', str(TEST_PORT)])
    def test_parse_params_all_params_passed(self):
        self.assertEqual(self.server.parse_params(), ('127.0.0.1', 8080))

    def test_get_response_message_200(self):
        resp_code_200 = {
            "response": 200,
            "alert": "Подключение прошло успешно"
        }
        presence_message = {
            "action": "presence",
            "time": self.time,
            "type": "status",
            "user": {
                "account_name": "kiki159",
                "status": "Online!"
            }
        }
        self.assertEqual(self.server.get_response_message(presence_message), resp_code_200)

    def test_get_response_message_400(self):
        resp_code_400 = {
            "response": 400,
            "alert": "Ошибка при подключении"
        }
        presence_message = {
            "action": "presence",
            "type": "status",
            "user": {
                "account_name": "kiki159",
                "status": "Online!"
            }
        }
        self.assertEqual(self.server.get_response_message(presence_message), resp_code_400)


if __name__ == '__main__':
    unittest.main()
