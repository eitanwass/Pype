import sys
import os

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
    dirname = os.path.dirname(__file__)
    file_path = os.path.join(dirname, "../dat/bridge_peers.dat")

    bridge_peers = Utils.get_addrs_from_file(file_path)
    user.connector.request_peers(bridge_peers[0])

