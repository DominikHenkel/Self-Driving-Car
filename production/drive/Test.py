import socket
import sys
import threading
import cv2
import numpy as np
import time
import copy
from ObjectDetector import Detector
from random import randint

det = Detector()
while True:
    then = time.time()
    path = "C:/Users/jalak/Desktop/car/Self-Driving-Car/production/drive/pics/0" + str(1021) + ".jpg"
    frame = cv2.imread(path,-1)
    result = det.process_img(frame)
    print(time.time() -then)
