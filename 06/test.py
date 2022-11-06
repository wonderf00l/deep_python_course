import unittest
from client import Client


class MyTestCase(unittest.TestCase):
    """server.py -p 1501 -w 8(any) -k 5"""


def test_server_valid_url(self):
    client = Client()
    client._port = 1501
    client._workers = 10
    client._file_path = "URL.txt"  # указание любого файла для корректного создания клиента
    client.client_configuration(("test", "valid"))  # алгоритм в случае теста - в start_interaction
    mock_arg = "unittest: {'https://www.python.org/': " \
               "{'and': 22, 'Python': 20, 'the': 18, 'to': 15}}"
    self.assertEqual(
        {'https://ru.wikipedia.org/wiki/Python': {'Python': 282,
                                                  'Архивировано': 163,
                                                  'Дата': 142,
                                                  'на': 184,
                                                  'обращения:': 137}},
        client.start_interaction()
    )


def test_server_invalid_url(self):
    client = Client()
    client._port = 1501
    client._workers = 10
    client._file_path = "URL.txt"
    client.client_configuration(("test", "invalid"))
    self.assertEqual(
        "'invalid test' -- INVALID URL",
        client.start_interaction()
    )


if __name__ == '__main__':
    unittest.main()
