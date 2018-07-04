#Erhält vom Controller, wie das Lenkrad gerade gedreht ist.

"""
Ausführen :
Zuerst diese Datei [wago_controller_pc.py] ausführen ohne Argumente.
Anschließend [wago_controller.py] ausführen ohne Argumente.
evtl. muss in [wago_controller.py] die IP in "client_socket.connect()" angepasst werden.
"""


import io
import socket
import struct
import sys


server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)


connection = server_socket.accept()[0].makefile('rwb')

print('Client connected!')
while(True):
    try:
        #Wenn du nicht weißt, wie "struct" funktioniert solltest du dir die Docs dazu durchlesen.
        #Erklären wäre zu kompliziert. Wir nutzen es einfach um dem Server zu senden wieviele Bytes
        #das nächste Paket groß ist, damit er weiß wieviele Bytes er lesen soll.
        response_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        #Ich frage nach länge 1 und 2. da Gradzahlen unter 10 logischerweise einstellig und über 10 zweistellig sind.
        if response_len == 1:
            string = connection.read(response_len).decode("utf-8")
            if(string == 'x'):
                print('Received signal to close connection!')
                connection.close()
                break
            degree = int(string)
            print(degree)
            #degree ist nun der drehungswert um den wir das lenkrad gedreht haben.
            #Die Zahl wird dann noch zusammen mit dem Input Bild abgespeichert.
            #Der OpenCV2 Code für die Kamera ist hier nicht mit bei, da ich nicht wusste,
            #ob du eine Kamera hast und OpenCV etc. Zudem ist das für dich ja auch nicht
            #relevant.
        elif response_len == 2:
            string = connection.read(response_len).decode("utf-8")
            degree = int(string)
            print(degree)
            #degree ist nun der drehungswert um den wir das lenkrad gedreht haben.
            #Die Zahl wird dann noch zusammen mit dem Input Bild abgespeichert.
            #Der OpenCV2 Code für die Kamera ist hier nicht mit bei, da ich nicht wusste,
            #ob du eine Kamera hast und OpenCV etc. Zudem ist das für dich ja auch nicht
            #relevant.
        else:
            print('Received string with length ',response_len, ' expected length 1 or 2. Content of  string: ', connection.read(response_len))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        break
print('Client connection closed!')
