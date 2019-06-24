import sys

from Connector import *
import Utils


class User():
    def __init__(self):
        if len(sys.argv) == 1:
            self.port = input('PORT >> ')
        else:
            self.port = sys.argv[1]

        # TODO: Perform checks

        self.peer_managers = []

        self.connector = Connector(self, self.port)


if __name__ == '__main__':
    user = User()

    # TODO: Try to connect to known peers

    # Try to connect to bridge peers
    bridge_peers = Utils.get_addrs_from_file("bridge_peers.txt")
    user.connector.request_peers(bridge_peers[0])

