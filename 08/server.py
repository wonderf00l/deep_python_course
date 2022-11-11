import getopt
import sys
from time import time
import socket
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
        self._clients = None
        self._server_sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self._queue = Queue()
        
    def server_configuration(self):
        try:
            opts = getopt.getopt(sys.argv[1:], "p:c:",
                                 ["port=", "clients="])[0]
        except getopt.GetoptError as error:
            print(error)
        try:
            for opt, arg in opts:
                if opt in ["-p", "--port"]:
                    self._port = int(arg)
                if opt in ["-c", "--clients"]:
                    self._clients = int(arg)
            if not self._port or not self._clients:
                raise ValueError
        except ValueError:
            while True:
                try:
                    print("Input correct parameters")
                    self._port = int(input("port: "))
                    self._workers = int(input("clients num: "))
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
        
def request_processing(self, client_sock, url):
    while True:
       try:
          data = requests.get(url, timeout=8)
          soup = BeautifulSoup(data.content, "html.parser")
          lst = soup.text.replace('\n', '').split(' ')
          lst_of_words = [word for word in lst if len(word) > 1]
          words_rate = {url: dict(Counter(lst_of_words).most_common(self._k_words))}
          json_doc = json.dumps(words_rate)
          client_sock.sendall(json_doc.encode(encoding="utf-8"))
          except requests.exceptions.MissingSchema:
          print("invalid URL")
          json_doc = json.dumps(f"{repr(url)} -- INVALID URL")
          client_sock.sendall(json_doc.encode(encoding="utf-8"))


if __name__ == '__main__':
    server = Server()
    server.server_configuration()
    server.serve_client()
