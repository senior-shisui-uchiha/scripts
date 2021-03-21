#!usr/bin/env python

# Only for python <2.7

import netfilterqueue


def process_packet(packet):
    print(packet)
    packet.accept()
# packet.drop() - drop packets
# packet.accept() - allow packet transfer


try:
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()
except KeyboardInterrupt:
    print("[+] Detected Ctrl+C ... Quitting ... Resetting ARP Tables")
