# example 1 (UDP client socket )
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 1 Create socket UDP(SOCK_DGRAM, for TCP SOCK_STREAM)
sock.sendto(b'Test message', ('localhost', 8888))        # 2 Send message to server
