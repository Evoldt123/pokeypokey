import socket
from _thread import *
import sys
import pickle
from poker_game import Game

# 172.26.101.220 for laptop
# 172.16.0.106 for PC
server = "25.63.113.238"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

id_count = 0
ids = [False for _ in range(7)]

game = []


def threaded_client(conn, id):
    global id_count
    global ids
    conn.send(str.encode(str(id)))

    # print("Connected to:", addr)

    reply = ""
    while True:
        try:
            data = conn.recv(2048*2)
            reply = data.decode("utf-8")

            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", reply)
                # print("Sending : ", reply)

                conn.sendall(pickle.dumps(game[0]))
        except:
            break

    print(f"ID {id} // Lost connection")

    if id == 0:
        print("Game Popped")
        game.pop()

    id_count -= 1
    ids[id] = False
    print("IDs are now", ids)
    print()
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to main:", addr)
    # Find available IDs
    new_id = -1
    for x in range(7): # Six Players rn
        if ids[x] == False:
            new_id = x
            id_count += 1
            ids[x] = True
            print(f"{addr} assigned ID {new_id}")
            print("IDs are now", ids, '\n')
            break

    if new_id == -1:
        print("Err: Probably max capacity")
        pass

    else:
        if new_id == 0:
            game.append(Game())
        # print("Connected to:", addr)

        start_new_thread(threaded_client, (conn, new_id))



