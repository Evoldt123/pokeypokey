import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 172.26.101.220 for laptop
        # 172.26.102.4 for PC? (confirm pls)
        self.server = "172.26.99.204"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.id = self.connect()
        # print(self.id)

    def getP(self):
        return self.id

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            print("err")
            pass

    def send(self, data):
        try:
            print(data)
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)