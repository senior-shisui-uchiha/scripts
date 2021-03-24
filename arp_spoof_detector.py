#!usr/bin/env python

import scapy.all as scapy

# Get ip and return mac in your network


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arb = broadcast/arp_request  # ARP request broadcast
    answered_list = scapy.srp(arb, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

# Looking for changes in ARP table


def process_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac = get_mac(packet[scapy.ARP].psrc)
            response_mac = packet[scapy.ARP].hwsrc
            if real_mac != response_mac:
                packet("[+] You under attack")
        except IndexError:
            pass


sniff("eth0")
