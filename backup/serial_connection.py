import serial
import sys
import threading
import re
import time

ser = serial.Serial( port='COM6',
         baudrate=115200,
         bytesize=serial.EIGHTBITS,
         parity=serial.PARITY_NONE,
         timeout=2)
try:

    print ("Serial port is open")
    ser.isOpen()

except Exception:

    print ("error open serial port: " + str(e))

    exit()

if ser.isOpen():
    try:
        ser.write('\r')
        ser.write('test')
        print("write data: reboot")

    except Exception:
        print ("error communicating...: " + str())
else:
    print ("cannot open serial port ")