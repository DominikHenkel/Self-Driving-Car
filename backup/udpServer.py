import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('',8000)
sock.bind(server_address)

print("Port " + str(server_address[1]) + " binded to " + server_address[0])

while True:
    print('receiving data...')
    data, address = sock.recvfrom(1024)
    sock.sendto(b'90' ,address)

    #print('received %s bytes from %s' % (len(data), address) + data)
    print("received message:", data)


    if data:
       sent = sock.sendto(data, address)
       print( 'sent %s bytes back to %s' % (sent, address))








#def Recv_handler():
#    quit = 'x'
#    while not quit == 'q':
#        print('receiving data...')
#        data, address = sock.recvfrom(1024)
#        quit = data
#
#        print('received %s bytes from %s' % (len(data), address))
#        print("received message:", data)
#        return(data, address)

#t = threading.Thread(target=Recv_handler).start()
#        print(t)
