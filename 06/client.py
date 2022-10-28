import socket
import sys
import getopt

class Client:
    def __init__(self):
        self._host = socket.gethostname()
        argv = sys.argv[1:]
        try:
            opts = getopt.getopt(argv, "p:", ["port="])[0]
        except getopt.GetoptError as error:
            print(error)
        for opt, arg in opts:
            if opt in ["-p", "--port"]:
                self._port = int(arg)
        self._client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self._client_sock.connect((self._host, self._port))
                break
            except OSError:
                print("Incorrect server port")
                self._port = int(input("Another port: "))

    def send_request(self):
        self._client_sock.send("https://www.google.com/webhp?hl=ru&sa=X&ved=0ahUKEwiYssbak4P7AhWhCRAIHY4ZAC0QPAgI".encode())

if __name__ == "__main__":
    client = Client()
    client.send_request()
