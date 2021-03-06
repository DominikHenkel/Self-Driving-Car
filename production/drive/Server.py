import socket
import sys
import threading
import cv2
import numpy as np
import time
import copy
from ObjectDetector import Detector
from random import randint

deg = 0
imageCopy = 0
result = []
person_left = False
x_old = -1
person_right = False
personLeft = False
personRight = False
maxSteeringAngle = 540

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('',1337)
sock.bind(server_address)

print("port " + str(server_address[1]) + " bound to " + server_address[0])

def camera():
    print('Starting cam thread')
    global result
    global deg
    global imageCopy
    global frame
    global x_old
    cap = cv2.VideoCapture(0)
    start = 1021
    secondTimer = time.time()
    fps = 0
    currentFps = 0
    resultCopy = []
    deg = 0
    id = 0
    act_car_x =0
    act_car_y =0
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
        min = 10000
        id = -1
        value = 0
        for i in range(len(resultCopy)):
            x = int(resultCopy[i][1])
            y = int(resultCopy[i][2])
            w = int(resultCopy[i][3] / 2)
            h = int(resultCopy[i][4] / 2)
            if(w*h > value):
                if(x_old == -1 or abs(x-x_old)<70):
                        x_old = x
                        value = w*h
                        id = i
            if(resultCopy[i][0]=="person"):
                cv2.rectangle(imageCopy, (x - w, y - h), (x + w, y + h), (0, 0, 139), 2)
                if(x>224):
                    personRight = True
                    personLeft = False
                else:
                    personRight = False
                    personLeft = True
            else:
                personRight = False
                personLeft = False
                cv2.rectangle(imageCopy, (x - w, y - h), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(
                 imageCopy, resultCopy[i][0] + ' : %.2f' % resultCopy[i][5],
                 (x - w + 5, y - h - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0, 0, 0), 1, lineType)
            # print('Person rechts', person_right, 'links', person_left)
        if(id!=-1):
            cv2.rectangle(imageCopy, (int(resultCopy[id][1]) - int(resultCopy[id][3] / 2), int(resultCopy[id][2]) - int(resultCopy[id][4] / 2)), (int(resultCopy[id][1]) + int(resultCopy[id][3] / 2), int(resultCopy[id][2]) + int(resultCopy[id][4] / 2)), (255, 0, 0), 2)
            print('Person rechts', personRight, 'Person links', personLeft)
        # if(len(resultCopy) != 0):
        #     degInner = int(getRotation(160, int(resultCopy[id][1])))
        #     degInner = int(getRotation(160,resultCopy[id][1]))
        # if(degInner != 0):
        #     deg = degInner
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
        imageCopy = cv2.resize(imageCopy,(1280,1024))
        cv2.imshow('Kamera + Neuronales Netz', imageCopy)
        # time.sleep(1.0)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def getRotation(maxAngle, x):
    return maxAngle*(((x/448)-0.5)/0.5)

def network():
    print('Starting network thread')
    data, address = sock.recvfrom(1000)
    print('connected ', address, ' ', data)
    startTime = 0
    endTime = 0
    timerStarted = False
    while True:
        # if(personLeft):
        #     if(timerStarted):
        #         deg = -maxSteeringAngle
        #     else:
        #         startTime = time.time()
        #         timerStarted = True
        # else:
        #     if(timerStarted):
        #         endTime = time.time()
        # elif(personRight):
        #     deg = maxSteeringAngle
        # else:
        path = "C:/Users/jalak/Desktop/car/Self-Driving-Car/production/drive/pics/02731.jpg"
        frame = cv2.imread(path,-1)
        cv2.imshow('asd', frame)
        k = cv2.waitKey(33)
        #print(k)
        if k == 49:
            sock.sendto(bytes(str(500),'utf-8'), address)
            time.sleep(1.2)
            sock.sendto(bytes(str(-500), 'utf-8'), address)
            time.sleep(2.8)
            sock.sendto(bytes(str(0),'utf-8'),address)
            time.sleep(1.2)
            print('finished')
            time.sleep(100)
        #elif k == -1:
        #    continue
        #print(did)
        #print(deg)

def map_t():
    print('Starting map thread')
    global map
    map = Map()
    while True:
        map.compute2DMap()

def nnw():
    det = Detector()
    global result
    while True:
        if(len(frame) != 0):
            result = det.process_img(frame)

#cam = threading.Thread(name='Camera', target=camera)
network = threading.Thread(name='Network', target=network)
#nnw = threading.Thread(name='nnw', target=nnw)

#cam.start()
network.start()
#nnw.start()
