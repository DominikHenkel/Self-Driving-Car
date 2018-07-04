import time
import socket

while True:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(1.0)
    message = b'25'
    addr = ("localhost", 8000)

    start = time.time()
    client_socket.sendto(message, addr)
    try:
        data, server = client_socket.recvfrom(131072)
        end = time.time()
        elapsed = end - start
        print(f'{data} {elapsed}')
    except socket.timeout:
        print('REQUEST TIMED OUT')
