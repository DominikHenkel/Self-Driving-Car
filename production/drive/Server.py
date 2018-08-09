import socket
import sys
import threading
import cv2
import numpy as np
import time
from test import Detector

cropped = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('',1337)
sock.bind(server_address)


#motor_data = []
#image_data = []

print("port " + str(server_address[1]) + " bound to " + server_address[0])

def camera():
    print('Starting cam thread')
    cap = cv2.VideoCapture(0)
    global cropped
    while True:
        ret, frame = cap.read()
        #resize  frame to needed size
        frame_size = (448,448)
        cropped = cv2.resize(frame, frame_size)
        #feed cropped frame into neural network
        cv2.imshow('frame',cropped)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def network():
    #waiting for client to connect. If more than one client look for another solution currently
    #only supports the test client
    print('Starting network thread')
    data, address = sock.recvfrom(100)
    while True:
        # data, address = sock.recvfrom(131072)
        # if(data.isdigit()):
        #     print('is degree')
        #     motor_data.append(data)
        # else:
        #     print('is image')
        #     image_data.append(data)
        # print("received message:", data)s

        #send neural network output here
        #we can acceess the global variable 'cropped' from here
        sock.sendto(b'90', address)
        time.sleep(1/20)
        #data abspeichern in einem array

def nnw():
    det = Detector()
    while True:
        det.process_img(cropped)
    return

def init_nnw():

    return


cam = threading.Thread(name='Camera', target=camera)
network = threading.Thread(name='Network', target=network)
nnw = threading.Thread(name='nnw', target=nnw)
nnw_init = threading.Thread(name='nnw_init', target=init_nnw)

cam.start()
network.start()
nnw_init.start()
nnw.start()
