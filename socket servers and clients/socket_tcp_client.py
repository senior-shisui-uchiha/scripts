#!/usr/bin/env python3
# Simple TCP client

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create TCP socket (SOCK_STREAM)
sock.connect(('ip', 8888))                                # Connect to ip and port 8888

sock.send(b'Test message')                                # Send message to server
result = sock.recv(64)
print('Response:', result)
sock.close()
