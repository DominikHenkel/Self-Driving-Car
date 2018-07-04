import socket
import sys
import random
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('',8000)
sock.bind(server_address)

print("port " + str(server_address[1]) + " bound to " + server_address[0])

print('awaiting connection...')
data, address = sock.recvfrom(131072)
print(f'{data}')

while True:
    degree = random.randint(-50,50)
    degreeS = str(degree)
    print('sending ', degree)
    sock.sendto(bytes(degreeS, "utf-8") , address)
    time.sleep(3)
    #data, address = sock.recvfrom(131072)
    #print("received answer:", data)
