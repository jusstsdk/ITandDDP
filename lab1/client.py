import socket
import threading
from datetime import datetime

name = input("Enter username: ")
sender_port = input("From: ")
receiver_port = input("To: ")

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("localhost", int(sender_port)))
print(f'\n{name} started from port {sender_port}\n')

try:
    f = open(f'{sender_port}_history.txt', 'r+')
except:
    f = open(f'{sender_port}_history.txt', 'w+')

print(f.read())


def receive():
    while True:
        try:
            _message, _ = client.recvfrom(1024)
            msg = _message.decode()
            if not msg.startswith("UP_TAG:") and not msg.startswith("OUT_TAG:"):
                print(msg[4:])
                f.write('\n' + msg[4:])
        except:
            pass


t = threading.Thread(target=receive)
t.start()

client.sendto(f"SIGNUP_TAG:{name}".encode(), ("localhost", 5555))

while True:
    message = input()
    if message == "!q":
        client.sendto(f"SIGNOUT_TAG:{name}".encode(), ("localhost", 5555))
        f.close()
        exit()
    else:
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        client.sendto(f"{receiver_port}{name}: <{now}> {message}".encode(), ("localhost", 5555))
        f.write('\n' + f"{name}: <{now}> {message}")
