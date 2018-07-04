"""AKTUELLER CODE FÜR DAS AUTO SOLL SPÄTER ZAHLEN AN DEN MOTOR SENDEN"""

import socket
import threading
import sys

s = socket.socket()
host = socket.gethostname()

port = 8000
s = socket.socket()
s.bind((host, port))
s.listen(5)

def processMessages(conn, addr):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                conn.close()
            print(data.decode("utf-8"))
        except:
            conn.close()
            print("Connection closed by", addr)
            # Quit the thread.
            sys.exit()


while True:
    # Wait for connections
    conn, addr = s.accept()
    print('Got connection from ', addr[0], '(', addr[1], ')')
    # Listen for messages on this connection
    listener = threading.Thread(target=processMessages, args=(conn, addr))
    listener.start()
