import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 172.26.101.220 for laptop
        # 172.16.0.106 for PC
        self.server = "25.63.113.238"
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
            # print(data)
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)