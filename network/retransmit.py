"""Retransmissão de pacotes via UDP para peers descobertos."""

import socket

from network.peer_discovery import get_peers

PORT = 50701


def retransmit_udp(packets: list[bytes]):
    peers = get_peers()
    if not peers:
        return
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for peer in peers:
        for pkt in packets:
            sock.sendto(pkt, (peer, PORT))
