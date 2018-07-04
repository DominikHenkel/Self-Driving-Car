import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('',8000)
sock.bind(server_address)

motor_data = []
image_data = []

print("port " + str(server_address[1]) + " bound to " + server_address[0])

while True:
    print('receiving data...')
    data, address = sock.recvfrom(131072)
    if(data.isdigit()):
        print('is degree')
        motor_data.append(data)
    else:
        print('is image')
        image_data.append(data)
    print("received message:", data)
    sock.sendto(b'90' , address)
    #data abspeichern in einem array
