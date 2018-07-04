import math
import socket
import sys
import threading
import time


# Create a UDP/IP Server
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('',8000)
sock.bind(server_address)

data = 'init'
address = ('0', 0)

# create sin wave
radValues = []
for degValue in range(0,361):
    degValue
    radValue = math.radians(degValue)
    radValues.append(radValue)

    sinValues = []
for rad in radValues:
    sinValue = math.sin(rad)
    sinValues.append(sinValue)
    

print("Port " + str(server_address[1]) + " binded to " + server_address[0])

i = 0
while True:
        if address[1] == 0:
            print('receiving data...')
            data, address = sock.recvfrom(1024)
            print('received %s bytes from %s' % (len(data), address))
            print("received message:", data)
        
        else:
            # simulate steering angle from -180° to 180° 
            if i < 360:
                steeringAngle = 180 * sinValues[i]
            else:
                i = 0
            i = i+1
            
            sent = sock.sendto(str(steeringAngle), address)
            print('sent %s bytes back to %s. Data: %u' % (sent, address, steeringAngle))
                
        time.sleep(0.1)
        