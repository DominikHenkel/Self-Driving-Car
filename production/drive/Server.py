import socket
import sys
import threading
import cv2
import numpy as np
import time
import copy
from ObjectDetector import Detector
from random import randint
from Map import Map
import threading

deg = 0
imageCopy = 0
result = []
map

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('',1337)
sock.bind(server_address)

print("port " + str(server_address[1]) + " bound to " + server_address[0])

def camera():
    global result
    global deg
    global imageCopy

    print('Starting cam thread')
    cap = cv2.VideoCapture(0)
    start = 1021
    secondTimer = time.time()
    fps = 0
    currentFps = 0
    resultCopy = []
    deg = 0
    while True:
        fps = fps +1
        if((time.time() -1) > secondTimer):
            secondTimer = time.time()
            print(fps)
            currentFps = fps
            fps = 0

        ret, frame = cap.read()
        frame = cv2.resize(frame,(448,448))
        start = start + 30
        path = "C:/Users/jalak/Desktop/car/Self-Driving-Car/production/drive/pics/0" + str(start) + ".jpg"
        #frame = cv2.imread(path,-1)
        imageCopy = copy.deepcopy(frame)
        resultCopy = copy.deepcopy(result)
        degInner = 0
        lineType = cv2.LINE_AA if cv2.__version__ > '3' else cv2.CV_AA
        for i in range(len(resultCopy)):
            x = int(resultCopy[i][1])
            y = int(resultCopy[i][2])
            w = int(resultCopy[i][3] / 2)
            h = int(resultCopy[i][4] / 2)
            map.add_entity(x,y,w,h,i,result[i][0],448)
            # cv2.rectangle(imageCopy, (x - w, y - h), (x + w, y + h), (0, 255, 0), 2)
            # cv2.rectangle(imageCopy, (x - w, y - h - 20),
            #               (x + w, y - h), (125, 125, 125), -1)
            # cv2.putText(
            #         imageCopy, resultCopy[i][0] + ' : %.2f' % resultCopy[i][5],
            #     (x - w + 5, y - h - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
            #     (0, 0, 0), 1, lineType)
            # degInner = int(getRotation(160,x))
            # print(degInner, "   ", x)
            #TODO only get deg of the car
        id = map.id
        cv2.rectangle(imageCopy, (resultCopy[id][1] - resultCopy[id][3] / 2, resultCopy[id][2] - resultCopy[id][4] / 2 - 20),
                       (resultCopy[id][1] + resultCopy[id][3] / 2, resultCopy[id][2] - resultCopy[id][4] / 2), (125, 125, 125), -1)
        cv2.putText(
             imageCopy, resultCopy[id][0] + ' : %.2f' % resultCopy[id][5],
             (resultCopy[id][1] - resultCopy[id][3] / 2 + 5, resultCopy[id][2] - resultCopy[id][4] / 2 - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
             (0, 0, 0), 1, lineType)
        degInner = int(getRotation(160,resultCopy[id][1]))

        if(degInner != 0):
            deg = degInner
        cv2.rectangle(imageCopy, (0,0),(1200,35),(0, 0, 0),-1)
        fpsString = "FPS: {}".format(currentFps)
        if(len(resultCopy) == 0):
            resultString = "NONE"
        else:
            resultString = resultCopy[0][0]
        if(deg < 0):
            wholeString = fpsString + " | Objekt: " + str(resultString) + " | Lenkrad: " + str(-deg) + " Grad nach links"
        elif(deg > 0):
            wholeString = fpsString + " | Objekt: " + str(resultString) + " | Lenkrad: " + str(deg) + " Grad nach rechts"
        else:
            wholeString = fpsString + " Kein Objekt erkannt"
        cv2.putText(imageCopy, str(wholeString), (5,23), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(50,150,250), 2, lineType)
        #time.sleep(3)
        cv2.imshow('Kamera + Neuronales Netz', cv2.resize(imageCopy,(1280,1024)))
        time.sleep(0.5)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def getRotation(maxAngle, x):
    return maxAngle*(((x/448)-0.5)/0.5)

def network():
    print('Starting network thread')
    data, address = sock.recvfrom(1000)
    print('connected ', address, ' ', data)
    while True:
        sock.sendto(bytes(str(deg),'utf-8'), address)
        time.sleep(1/60)

def map_t():
    global map
    map = Map()

def nnw():
    det = Detector()
    global result
    while True:
        result = det.process_img(imageCopy)

map = threading.Thread(name='Map', target=map_t)
cam = threading.Thread(name='Camera', target=camera)
network = threading.Thread(name='Network', target=network)
nnw = threading.Thread(name='nnw', target=nnw)

map.start()
cam.start()
network.start()
nnw.start()
