#!/usr/bin/env python3
# unix udp client
# Exchange point there is a file unix.sock
import socket

sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
sock.sendto(b'Test Message', 'unix.sock')
