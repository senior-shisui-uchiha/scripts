#!/usr/bin/env python

# 08:00:27:ab:08:1c
# For python 2.7

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest='interface', help='Interface witch you wanna change')
    parser.add_option('-m', '--mac_address', dest='mac_address', help='New MAC address witch you need')
    (options, arguments) = parser.parse_args()
    if not options:
        parser.error('[-] Please specify an arguments, use --help for more information')
    return options


def change_mac(interface, mac_address):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac_address])
    subprocess.call(["ifconfig", interface, "up"])
    print('[+] Change Mac Address for %s to %s' % (interface, mac_address))


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-]Could not read MAC Address")


options = get_arguments()

