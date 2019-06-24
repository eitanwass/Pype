import sys

from Connector import *


class Bridge():
    def __init__(self):
        # Bridge Default Port is 50_000
        self.port = 50_000

        self.connector = Connector(self.port)


if __name__ == '__main__':
    bridge = Bridge()

    print("Bridge is UP")