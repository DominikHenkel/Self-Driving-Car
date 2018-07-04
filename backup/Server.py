import io
import socket
import struct
from PIL import Image
import cv2
import numpy as np
import sys
import cnnModel
import tensorflow as tf
import os

training = True
restore = True

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)
output = [0,0,0]

motor_data = []
image_data = []


"""def load_file(filepath):
    training_data = []

    if(os.path.isfile(filepath+'.npy')):
        training_data = np.load(filepath+'.npy')
    return training_data

if(restore==False):

    motor_data = []
    image_data = []
else:
    image_data = load_file('D:\\Trainingsdaten\\image_data')
    motor_data = load_file('D:\\Trainingsdaten\\motor_data')
    print(len(image_data))
    print(len(motor_data))


motor_data = motor_data.tolist()
image_data = image_data.tolist()"""
connection = server_socket.accept()[0].makefile('rwb')


print('neuer Client')
while(True):
    try:
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if image_len>1:
            image = np.frombuffer(connection.read(image_len), dtype = np.uint8)
            image = np.reshape(image, (66,200,3))
            image_data.append([image])
            motor_data.append([output])
            cv2.imshow('Self driving car',image)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
        else:
            image = connection.read(image_len).decode('utf-8')
            print(image)
            output = [0,0,0]
            if(image == '2'):
                output = np.asarray([0,1,0])
            elif(image == '3'):
                output = np.asarray([0,0,1])
            elif(image == '4'):
                output = np.asarray([1,0,0])
    except:
        print("Unexpected error:", sys.exc_info()[0])
        break
print('closed')
connection.close()
print('Aufnahmelänge: ',str(len(motor_data)), str(len(image_data)))
np.save('D:\\Trainingsdaten\\image_data', image_data)
np.save('D:\\Trainingsdaten\\motor_data', motor_data)
print('saved')
server_socket.close()
