import socket
import time

address = ('localhost', 10000)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(address)
sock.listen()

while True:
    print("I am a WIP server")
    time.sleep(2)
