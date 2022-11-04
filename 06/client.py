import json
import queue
import socket
import sys
import getopt
from queue import Queue
import threading
from time import time


class Client:
    def __init__(self):
        self._host = socket.gethostname()
        try:
            opts = getopt.getopt(sys.argv[1:], "p:w:f:", ["port=", "workers=", "file="])[0]
        except getopt.GetoptError as error:
            print(error)
        try:
            for opt, arg in opts:
                if opt in ["-p", "--port"]:
                    self._port = int(arg)
                if opt in ["-w", "--workers"]:
                    self._workers = int(arg)
                if opt in ["-f", "--file"]:
                    self._file_path = arg
            if not self._port or not self._workers:
                raise ValueError
        except ValueError:
            while True:
                try:
                    print("Input correct parameters")
                    self._port = int(input("port: "))
                    self._workers = int(input("workers: "))
                    break
                except ValueError:
                    continue
        try:
            if not self._file_path:
                raise FileNotFoundError
            self._file = open(self._file_path, 'r', encoding="utf-8")
        except FileNotFoundError:
            while True:
                try:
                    print(f"Incorrect file path: {self._file_path}")
                    self._file_path = input("New file path: ")
                    self._file = open(self._file_path, 'r', encoding="utf-8")
                    break
                except FileNotFoundError:
                    continue
        self._queue = Queue()
        self._lock = threading.Lock()
        self._is_new = ''

    def set_connection(self, client_sock):
        while True:
            try:
                client_sock.connect(
                    ("127.0.0.1", self._port)
                )
                break
            except OSError as error:
                print(error)
                while True:
                    try:
                        self._port = int(input("Another port: "))
                        break
                    except ValueError:
                        print("Input correct port")

    def start_interaction(self):
        while True:
            client_sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )
            start = time()
            self.set_connection(client_sock)
            print(self._port, self._workers, self._file_path)
            i_list = iter(self._file.readlines())
            for string in i_list:
                if string == '\n':
                    break
                for _ in range(0, 100):
                    self._queue.put(string)
            for string in i_list:
                self._queue.put(string)
            if not self._queue.empty():
                threads = [threading.Thread(
                    target=Client.send_url,
                    args=(self, client_sock)
                ) for _ in range(self._workers)]
                for thread in threads:
                    thread.start()
                for thread in threads:
                    thread.join()
            self._file.close()
            client_sock.close()
            end = time()
            print(f"End of the session on the client, time: {end - start}\n")
            while True:
                retry = input("Retry connection? (Y/N)")
                if retry in ['Y', 'y']:
                    while True:
                        self._is_new = input("Would you like to change file? (Y/N)")
                        if self._is_new in ['Y', 'y']:
                            while True:
                                new_path = input("Input new file name:")
                                try:
                                    self._file = open(new_path, 'r', encoding="utf-8")
                                    break
                                except FileNotFoundError:
                                    print("Incorrect file name")
                                    continue
                        if self._is_new in ['N', 'n']:
                            self._file = open(self._file_path, 'r', encoding="utf-8")
                            break
                        if self._is_new in ['Y', 'y'] or self._is_new in ['N', 'n']:
                            break
                        continue
                if retry in ['N', 'n']:
                    raise ConnectionError("Work of the client has been stopped")
                if self._is_new in ['Y', 'y'] or self._is_new in ['N', 'n']:
                    break
                continue

    def send_url(self, client_sock):
        while True:
            try:
                to_send = self._queue.get(timeout=2)
                with self._lock:
                    print(f"Thread {threading.get_ident()} got {to_send} from queue")
                client_sock.send(to_send.encode())
                with self._lock:
                    print(f"Thread {threading.get_ident()} sent url")
                data = client_sock.recv(
                    1024)
                with self._lock:
                    pass
                decoded_data = json.loads(data.decode())
                with self._lock:
                    print(f"Thread {threading.get_ident()} received stat:\n{decoded_data}")
                if not data:
                    raise ConnectionError
            except queue.Empty:
                with self._lock:
                    print(f"Thread {threading.get_ident()} status: "
                          f"no URLs left to send, dying")
                    break
            except ConnectionError:
                with self._lock:
                    print(f"Server doesn't send statistics "
                          f"to thread {threading.get_ident()} anymore")


if __name__ == "__main__":
    client = Client()
    client.start_interaction()
