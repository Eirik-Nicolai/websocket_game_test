import socket
import sys
from _thread import *

server = "192.168.0.4"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

print("set up server")

s.listen(2)
print("Listening...")

def read_pos(str):
    val = str.split(',')
    return int(val[0]),int(val[1])

def make_pos(pos):
    return str(pos[0]) + "," + str(pos[1])

pos = [(0,0), (150,150)]

def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data

            if not data:
                break
            else:
                if player == 0:
                    reply = pos[1]
                else:
                    reply = pos[0]


                conn.sendall(str.encode(make_pos(reply)))

        except socket.error as e:
            print("error 3 ", e)
            break
    print("Terminating connection")
    conn.close()

current_player = 0
while True:
    conn, addr = s.accept()
    print("Connected to ", addr)

    start_new_thread(threaded_client, (conn, current_player))
    current_player += 1
