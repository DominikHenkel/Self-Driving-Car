"""AKTUELLER CODE FÜR DAS AUTO SOLL SPÄTER ZAHLEN AN DEN MOTOR SENDEN"""

import socket

host = socket.gethostname()
port = 8000
conn = socket.socket()

conn.connect((host, port))

conn.sendall(b'Connected. Waiting for data...')
intosend = input("message to send:")
conn.sendall(bytes(intosend, 'utf-8'))

data = conn.recv(1024)
intosend= "no"

while intosend != "quit":
    intosend = input("message to send:")
    conn.sendall(bytes(intosend, 'utf-8'))



conn.close()


print(data.decode("utf-8"))
