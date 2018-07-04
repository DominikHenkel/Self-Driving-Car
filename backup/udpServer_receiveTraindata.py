import math
import socket
import sys


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = ('',8000)
sock.bind(server_address)

data = 'init'
address = ('0', 0)
    
print("Port " + str(server_address[1]) + " binded to " + server_address[0])

while True:
    print('receiving data...')
    data, address = sock.recvfrom(1024)
    print('received %s bytes from %s' % (len(data), address))
    print('received message: %s' % data)