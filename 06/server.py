import getopt
import sys
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
        argv = sys.argv[1:]
        try:
            opts = getopt.getopt(argv, "p:w:k:",
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
        self._server_sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        while True:
            try:
                self._server_sock.bind((self._host, self._port))
                break
            except OSError:
                print("Address already in use, try another")
                self._port = int(input("Another port: "))
        self._server_sock.listen()
        self._queue = Queue()
        self._lock = threading.Lock()

    def serve_client(self):
        while True:
            client_sock, client_addr = self._server_sock.accept()
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
                        char = client_sock.recv(1).decode()
                        if char == '\n':
                            break
                        if not char:
                            raise ConnectionError
                        data += char
                    print(f"data: {data}")
                    self._queue.put(data)
            except ConnectionError:
                print("No data to receive")
            for thread in threads:
                thread.join()
            client_sock.close()
            print("End of the session on the server\n")

    def request_processing(self, client_sock, stat):
        while True:
            try:
                url = self._queue.get(timeout=5)
                with self._lock:
                    print(f"Thread {threading.get_ident()} has started processing {url}")
                data = requests.get(url, timeout=8)
                soup = BeautifulSoup(data.text, "lxml")
                lst = soup.text.replace('\n', '').split(' ')
                lst_of_words = [word for word in lst if len(word) > 1]
                # lst_of_words = filter(self.func, lst)
                words_rate = dict(Counter(lst_of_words).most_common(self._k_words))
                json_doc = json.dumps(words_rate)
                client_sock.sendall(json_doc.encode(encoding="utf-8"))
                with self._lock:
                    # client_sock.sendall(json_doc.encode(encoding="utf-8")) # is this thread-safe?
                    stat.put(json_doc)
                    print(f"{stat.qsize()} URLs have been processed")
            except queue.Empty:
                with self._lock:
                    print("Queue is empty, no URLs to process")  
                    print(f" Thread {threading.get_ident()} isn't alive anymore")
                    break
            except ConnectionError:
                print("Client suddenly closed tne connection")

    # @staticmethod
    # def func(word):
    #     try:
    #         ord(word)
    #     except TypeError:
    #         return True


if __name__ == '__main__':
    server = Server()
    server.serve_client()
