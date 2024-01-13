import getopt
import sys
from time import time
import socket
import threading
import queue
from queue import Queue
from collections import Counter
import json
import requests
from bs4 import BeautifulSoup


class Server:

    def __init__(self):
        self._host = socket.gethostname()
        self._port = None
        self._workers = None
        self._k_words = None
        self._server_sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self._queue = Queue()
        self._lock = threading.Lock()

    def server_configuration(self):
        try:
            opts = getopt.getopt(sys.argv[1:], "p:w:k:",
                                 ["port=", "workers="])[0]
        except getopt.GetoptError as error:
            print(error)
        try:
            for opt, arg in opts:
                if opt in ["-p", "--port"]:
                    self._port = int(arg)
                if opt in ["-w", "--workers"]:
                    self._workers = int(arg)
                if opt in ["-k"]:
                    self._k_words = int(arg)
            if not self._port or not self._workers or not self._k_words:
                raise ValueError
        except ValueError:
            while True:
                try:
                    print("Input correct parameters")
                    self._port = int(input("port: "))
                    self._workers = int(input("workers: "))
                    self._k_words = int(input("number of words: "))
                    break
                except ValueError:
                    continue
        while True:
            try:
                self._server_sock.bind(("127.0.0.1", self._port))
                break
            except OSError:
                print("Address already in use, try another")
                self._port = int(input("Another port: "))
        self._server_sock.listen()

    def serve_client(self):
        while True:
            print("Waiting for the clients...")
            client_sock, client_addr = self._server_sock.accept()
            start = time()
            print(f"{client_addr} has connected to the server")
            stat = Queue()
            threads = [threading.Thread(
                target=Server.request_processing,
                args=(self, client_sock, stat)
            ) for _ in range(self._workers)]
            for thread in threads:
                thread.start()
            try:
                while True:
                    data = ''
                    while True:
                        client_sock.settimeout(2)
                        char = client_sock.recv(1).decode()
                        if char == '\n':
                            break
                        if not char:
                            raise ConnectionError
                        data += char
                    if data:
                        self._queue.put(
                            data)
            except ConnectionError:
                print("recv() got None,"
                      "no data to receive anymore")
            except TimeoutError as error:
                print(f"recv() status: {error}, "
                      f"no data to receive")
            for thread in threads:
                thread.join()
            client_sock.close()
            end = time()
            print(f"End of the session on the server, time: {end - start}\n")

    def request_processing(self, client_sock, stat):
        while True:
            try:
                url = self._queue.get(
                    timeout=5)
                with self._lock:
                    print(f"Thread {threading.get_ident()} "
                          f"has started processing {url}")
                data = requests.get(url, timeout=8)
                soup = BeautifulSoup(data.content, "html.parser")
                lst = soup.text.replace('\n', '').split(' ')
                lst_of_words = [word for word in lst if len(word) > 1]
                words_rate = {url: dict(Counter(lst_of_words).most_common(self._k_words))}
                json_doc = json.dumps(words_rate)
                client_sock.sendall(json_doc.encode(encoding="utf-8"))
                print(f"{threading.get_ident()} "
                      f"has sent {url} stat to the client")
                stat.put(json_doc)
                with self._lock:
                    print(f"{stat.qsize()} valid URLs have been processed")
            except queue.Empty:
                with self._lock:
                    print(f"Queue is empty, "
                          f"thread {threading.get_ident()} isn't alive anymore")
                break
            except requests.exceptions.MissingSchema:
                with self._lock:
                    print(f"Thread {threading.get_ident()} got "
                          f"invalid URL!")
                json_doc = json.dumps(f"{repr(url)} -- INVALID URL")
                client_sock.sendall(json_doc.encode(encoding="utf-8"))


if __name__ == '__main__':
    server = Server()
    server.server_configuration()
    server.serve_client()
