#!/usr/bin/env python3

# 04:d4:c4:ec:39:b8 -my real MAC address
# Script scan network, all new MAC address will be insert into DB(MariaDB)
# Script can change MAC address, it will be MAC address witch you input with key -m(--mac_address)
# or script generate new random MAC address
# Key -i is required, Script can`t work without key -i
# How does it work.
# You input required interface. Script find ip address of this interface and start to scan network
# After scan all new MAC address insert to DB , in the end you can change your MAC address
# Random MAC address
# P.S. if you don`t connect to network you also can change MAC address

import scapy.all as scapy
from tabulate import tabulate
import argparse
import mariadb
import sys
import random
import subprocess
import re


# Interface is important argument, you must choice it, or script will close

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interface',   dest='interface',   help='Interface witch you choice for scan')
    parser.add_argument('-m', '--mac_address', dest='mac_address', help='MAC address if you do not need random mac')
    option = parser.parse_args()
    if not option.interface:
        parser.error('[-] Please specify an arguments, use --help for more information')
        exit()
    return option


# It get interface IP for scan

def get_ip(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    ip_address_search_result = re.search(r"", ifconfig_result)
    if ip_address_search_result:
        return ip_address_search_result.group(0)
    else:
        print("[-]Could not read IP Address")


# Create cursor to DB

def create_cursor(login, password, db):
    try:
        conn = mariadb.connect(
            user=login,
            password=password,
            host="127.0.0.1",
            port=3306,
            database=db
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    return conn


# It scan network

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


# For pretty output result

def print_result(client_list):
    answers = []
    t = 1
    table_header = ["№", "IP", "MAC Address"]
    for item in client_list:
        answers.append([t, item["ip"], item["mac"]])
        t += 1
    print(tabulate(answers, table_header))


# It looking for MAC address from scan result in Database and add new MAC addresses into table

def update_table(client_list):
    print("[+] Updating database ...")
    records = []
    rec_count = 0
    cursor.execute("SELECT * FROM IP_and_MAC")
    for i, ip_address, mac_address in cursor:
        records.append(f"{mac_address}")
    try:
        for client in client_list:
            if str(client['mac']) in records:
                rec_count += 1
            else:
                cursor.execute("INSERT INTO IP_and_MAC (ip_address,mac_address) VALUES (?, ?)",
                               (str(client["ip"]), str(client["mac"]),))
    except mariadb.Error as error:
        print(f"Error: {error}")
    print("[+] You have %s MAC address from this network in your Database" % rec_count)
    print(f"Last Inserted ID: {cursor.lastrowid}")
    connection.commit()
    connection.close()


# Generate new random MAC address . Next function change MAC

def random_mac():
    mac_address = ':'.join('%02x' % random.randrange(256) for _ in range(5))
    return mac_address


def change_mac(interface, mac_address):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac_address])
    subprocess.call(["ifconfig", interface, "up"])
    print('[+] Change Mac Address for %s to %s' % (interface, mac_address))


# It get you MAC address from ifconfig result

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC Address")


# START PROGRAM #

options = get_arguments()
connection = create_cursor("oscar", "P2swVy7jvr", "Network")
cursor = connection.cursor()
# network = get_ip(options.interface)
network = '192.168.43.0/24'
scan_result = scan(network)
if not scan_result:
    print("[+] You does not connect to network ...")
else:
    print_result(scan_result)
    update_table(scan_result)

# if MAC address was not choice script can generate new random MAC address

if not options.mac_address:
    while True:
        answer = input("[+] Put new random MAC address ?(y/n)")
        if answer.lower() == "n" or answer.lower() == "no":
            break
        elif answer.lower() == "y" or answer.lower() == "yes":
            current_mac = get_current_mac(options.interface)
            print("Current Mac -> " + str(current_mac))
            new_mac = random_mac()
            change_mac(options.interface, new_mac)
            current_mac = get_current_mac(options.interface)
            if new_mac == current_mac:
                print("[+] MAC address was successfully change to " + current_mac)
            break
        else:
            print("[-] Try again")
else:
    current_mac = get_current_mac(options.interface)
    print("Current Mac -> " + str(current_mac))
    change_mac(options.interface, options.mac_address)
    current_mac = get_current_mac(options.interface)
    if current_mac == options.mac_address:
        print("[+] MAC address was successfully change to " + current_mac)
