import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "10.10.0.37"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()
        # self.isExit = False

    def getP(self):
        return self.p
    
    # def getExit(self):
    #     self.isExit = True
    #     return self.isExit

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)