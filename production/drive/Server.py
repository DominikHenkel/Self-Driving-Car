import socket
import sys
import threading
import cv2
import numpy as np
import time
from test import Detector

cropped = 0
result = []

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
    global result
    while True:
        ret, frame = cap.read()
        frame_size = (448,448)
        cropped = cv2.resize(frame, frame_size)
        cropped = cv2.flip( cropped, 0 )
        # print(result)
        for i in range(len(result)):
            x = int(result[i][1])
            y = int(result[i][2])
            w = int(result[i][3] / 2)
            h = int(result[i][4] / 2)
            cv2.rectangle(cropped, (x - w, y - h), (x + w, y + h), (0, 255, 0), 2)
            cv2.rectangle(cropped, (x - w, y - h - 20),
                          (x + w, y - h), (125, 125, 125), -1)
            lineType = cv2.LINE_AA if cv2.__version__ > '3' else cv2.CV_AA
            cv2.putText(
                cropped, result[i][0] + ' : %.2f' % result[i][5],
                (x - w + 5, y - h - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 0, 0), 1, lineType)
            print(getRotation(160,x))

        cv2.imshow('Image', cropped)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        #feed cropped frame into neural network
def getRotation(maxAngle, x):
    return maxAngle*(((x/448)-0.5)/0.5)

def network():
    #waiting for client to connect. If more than one client look for another solution currently
    #only supports the test client
    print('Starting network thread')
    data, address = sock.recvfrom(100)
    while True:
        sock.sendto(b'90', address)
        time.sleep(1/20)
        data, address = sock.recvfrom(131072)
        if(data.isdigit()):
            print('is degree')
            #motor_data.append(data)
        else:
            print('is image')
            #image_data.append(data)
        print("received message:", data)


#def draw_result(img, result):
    # for i in range(len(result)):
    #     x = int(result[i][1])
    #     y = int(result[i][2])
    #     w = int(result[i][3] / 2)
    #     h = int(result[i][4] / 2)
    #     cv2.rectangle(img, (x - w, y - h), (x + w, y + h), (0, 255, 0), 2)
    #     cv2.rectangle(img, (x - w, y - h - 20),
    #                   (x + w, y - h), (125, 125, 125), -1)
    #     lineType = cv2.LINE_AA if cv2.__version__ > '3' else cv2.CV_AA
    #     cv2.putText(
    #         img, result[i][0] + ' : %.2f' % result[i][5],
    #         (x - w + 5, y - h - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
    #         (0, 0, 0), 1, lineType)


def nnw():
    det = Detector()
    global result
    while True:
        result = det.process_img(cropped)
        #draw_result(cropped, det.process_img(cropped))
        #print(time.time() - timeThen)

    return


cam = threading.Thread(name='Camera', target=camera)
network = threading.Thread(name='Network', target=network)
nnw = threading.Thread(name='nnw', target=nnw)

cam.start()
network.start()
nnw.start()
