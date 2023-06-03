import unittest
import sys
import os
from unittest.mock import patch

sys.path.append(os.getcwd())
from client import Client


class TestClient(unittest.TestCase):

    TEST_ADDR = '127.0.0.1'
    TEST_PORT = 8080

    @patch('sys.argv', ['', TEST_ADDR, str(TEST_PORT)])
    def test_parse_params_all_params_passed(self):
        self.assertEqual(Client.parse_params(), ('127.0.0.1', 8080))


if __name__ == '__main__':
    unittest.main()
