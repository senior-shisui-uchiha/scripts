#!/usr/bin/env python3


# ░███╗░░██╗███████╗████████╗░██╗░░░░░░░██╗░█████╗░██████╗░██╗░░██╗░░░░░░░██████╗░█████╗░░█████╗░███╗░░██╗░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░████╗░██║██╔════╝╚══██╔══╝░██║░░██╗░░██║██╔══██╗██╔══██╗██║░██╔╝░░░░░░██╔════╝██╔══██╗██╔══██╗████╗░██║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░██╔██╗██║█████╗░░░░░██║░░░░╚██╗████╗██╔╝██║░░██║██████╔╝█████═╝░░░░░░░╚█████╗░██║░░╚═╝███████║██╔██╗██║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░██║╚████║██╔══╝░░░░░██║░░░░░████╔═████║░██║░░██║██╔══██╗██╔═██╗░░░░░░░░╚═══██╗██║░░██╗██╔══██║██║╚████║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░██║░╚███║███████╗░░░██║░░░░░╚██╔╝░╚██╔╝░╚█████╔╝██║░░██║██║░╚██╗░░░░░░██████╔╝╚█████╔╝██║░░██║██║░╚███║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░╚═╝░░╚══╝╚══════╝░░░╚═╝░░░░░░╚═╝░░░╚═╝░░░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝░░░░░░╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚══╝░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░


import scapy.all as scapy
from tabulate import tabulate
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest='target', help='Target IP / IP range')
    option = parser.parse_args()
    if not option:
        parser.error('[-] Please specify an arguments, use --help for more information')
    return option


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arb = broadcast/arp_request  # ARP request broadcast
    answered_list = scapy.srp(arb, timeout=1, verbose=False)[0]
    client_list = []
    for item in answered_list:
        client_dict = {"ip": item[1].psrc, "mac": item[1].hwsrc}
        client_list.append(client_dict)
    return client_list


def print_result(client_list):
    answers = []
    t = 1
    table_header = ["№", "IP", "MAC Address"]
    for item in client_list:
        answers.append([t, item["ip"], item["mac"]])
        t += 1
    print(tabulate(answers, table_header))


print("█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗")
print("╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝")
options = get_arguments()
scan_result = scan('192.168.136.0/24')
print_result(scan_result)
print("█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗")
print("╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝")
