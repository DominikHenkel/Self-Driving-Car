import time
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(10.0)
message = b'CONNECTED'
addr = ("localhost", 8000)

start = time.time()
client_socket.sendto(message , addr)
try:
    while True:
        data, server = client_socket.recvfrom(131072)
        end = time.time()
        elapsed = end - start
        print(f'{data}')
except socket.timeout:
    print('REQUEST TIMED OUT')
