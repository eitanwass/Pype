import socket

from Generic_Packed_Data import *


class PeerManager():
    def __init__(self):
        # Create Peer Socket
        self.peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return

    def host(self, port=0):
        self.peer_socket.bind(('', port))
        self.peer_socket.listen(1)
        self.peer_socket, addr = self.peer_socket.accept()
        return

    def connect(self, addr):
        self.peer_socket.connect(addr)
        self.peer_socket.sendall('test'.encode())
        return

    def run(self):
        while True:
            data = self.peer_socket.recv(1024)
            print(data.decode())
        return
