#Soll in die Sprache des Controllers übersetzt werden und die Motordrehung auslesen
#Sendet anschließend an den Server die Drehung

"""
Ausführen :
Zuerst die Datei [wago_controller_pc.py] ausführen ohne Argumente.
Anschließend diese Datei [wago_controller.py] ausführen ohne Argumente.
evtl. muss in [wago_controller.py] die IP in "client_socket.connect()" angepasst werden.
"""

import io
import socket
import struct

client_socket = socket.socket()
client_socket.connect(('192.168.2.108', 8000))
connection = client_socket.makefile('rwb')

#Zum testen. sendet erst eine 25 dann eine 7 und dann ein 'x' welches die Verbindung beendet

def main():
    send('25')
    send('7')
    endConnection()


def send(content):
    #Wenn du nicht weißt, wie "struct" funktioniert solltest du dir die Docs dazu durchlesen.
    #Erklären wäre zu kompliziert. Wir nutzen es einfach um dem Server zu senden wieviele Bytes
    #das nächste Paket groß ist, damit er weiß wieviele Bytes er lesen soll.
    connection.write(struct.pack('<L', len(content)))
    connection.flush()
    connection.write(bytes(content,'utf8'))
    connection.flush()

def endConnection():
    send('x')



if __name__ == '__main__':
    main()
