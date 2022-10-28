import requests
from bs4 import BeautifulSoup
import getopt
import sys
import socket
import threading
from queue import Queue


class Server:

    def __init__(self):  # port - command line arg
        self._host = socket.gethostname()
        argv = sys.argv[1:]
        try:
            opts = getopt.getopt(argv, "p:w:k:",
                                 ["port=", "workers="])[0]
        except getopt.GetoptError as error:
            print(error)
        for opt, arg in opts:
            if opt in ["-p", "--port"]:
                self._port = int(arg)
            if opt in ["-w", "--workers"]:
                self._workers = int(arg)
            if opt in ["-k"]:
                self._k_words = int(arg)
        self.server_sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        while True:
            try:
                self.server_sock.bind((self._host, self._port))
                break
            except OSError:
                print("Address already in use, try another")
                self._port = int(input("Another port: "))
        self.server_sock.listen()
        self.queue = Queue(20)
        self.sem = threading.Semaphore(self._workers)

    def serve_client(self=None):
        client_server_sock, client_addr = self.server_sock.accept()
        print(f"Got connection with {client_addr}")
        [threading.Thread(
            target=Server.request_processing,
            args=(self,) # another args
        ).start()
         for _ in range(self._workers)]
        try:
            while True:
                data = client_server_sock.recv(1024).decode()
                if not data:
                    break
                print(f"data: {data}")
                self.queue.put(data) 

        except ConnectionResetError:
            print("Lost connection")
        print("End of the session")

    def set_connection(self):
        client_server_sock, client_addr = self.server_sock.accept()
        print(f"Got connection with {client_addr}")
        return client_server_sock

    def request_processing(self, url):
        with self.sem:
            data = requests.get(url)
            soup = BeautifulSoup(data.text, "lxml")

    def print_statistics(self):
        pass

if __name__ == '__main__':
    server = Server()
    server.serve_client()
