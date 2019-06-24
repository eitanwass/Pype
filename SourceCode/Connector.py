import random
import socket
import threading
import json

from Generic_Packed_Data import *
from Peer_Manager import *


class Connector():
    def __init__(self, user, port):
        self.user = user

        self.known_peers = set()
        self.port = port

        # Create a UDP listener
        self.udp_listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_listener.bind(('', int(self.port)))
        threading.Thread(name='udp_listening', target=self.udp_listening, args=(self.udp_listener,)).start()


    def udp_listening(self, socket):
        while True:
            data, addr = socket.recvfrom(1024)

            self.known_peers.add(addr)

            data = data.decode()
            data = json.loads(data)
            data = GPD.rebuild(data)

            self.analyze_received_gpd(data, addr)

    
    def analyze_received_gpd(self, gpd, addr):
        gpd_title = gpd.title.upper()

        if gpd_title == 'PEER_OFFER':
            # Got offered a peer
            # TODO: Check if already has peer
            self.connection_request(gpd.content)

        elif gpd_title == 'PEER_REQ':
            # Addr requests peer
            if not self.send_peer_addr(addr):
                err_gpd = GPD('ERROR', 'No Peers to Share').to_json()
                self.udp_listener.sendto(err_gpd.encode(), addr)

        elif gpd_title == 'CON_REQ':
            # Addr requests to connect
            responder = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            responder.bind(('', 0))

            con_res_gpd = GPD('CON_RES').to_json()
            responder.sendto(con_res_gpd.encode(), addr)

            peer_manager = PeerManager()
            peer_manager.host(int(responder.getsockname()[1]))
            peer_manager.run()

            self.user.peer_managers.append(peer_manager)

        elif gpd_title == 'CON_RES':
            # Addr allows client to connect
            peer_manager = PeerManager()
            peer_manager.connect(addr)
            peer_manager.run()

        elif gpd_title == 'ERROR':
            # Received Error
            print('ERROR: ' + str(gpd.content))

        else:
            # Unidentified title
            print('UNIDENTIFIED TITLE: {}({})'.format(str(gpd_title), str(gpd.content)))
        return


    def request_peers(self, addr):
        peer_req_gpd = GPD('PEER_REQ', 1).to_json()
        self.udp_listener.sendto(peer_req_gpd.encode(), (addr[0], int(addr[1])))        # If IP and PORT
        return


    def connection_request(self, addr):
        addr = eval(addr)
        con_req_gpd = GPD('CON_REQ').to_json()
        self.udp_listener.sendto(con_req_gpd.encode(), addr)
        return

    
    def send_peer_addr(self, addr):
        for entry in self.known_peers:
            if entry != addr:
                peer_offer_gpd = GPD('PEER_OFFER', str(entry)).to_json()
                self.udp_listener.sendto(peer_offer_gpd.encode(), addr)
                print('Shared ' + str(entry) + ' with ' + str(addr))
                return True
        return False

