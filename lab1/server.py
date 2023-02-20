import socket
import threading
import queue

HOST, PORT = "localhost", 5555

messages = queue.Queue()

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

print("Server started")


def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)
            messages.put((message, addr))
        except:
            pass


def send():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            try:
                if message.decode().startswith("SIGNUP_TAG:"):
                    name = message.decode()[message.decode().index(":") + 1:]
                    print(f"{name} connected on {addr[1]}!")
                elif message.decode().startswith("SIGNOUT_TAG:"):
                    name = message.decode()[message.decode().index(":") + 1:]
                    print(f"{name} disconnected from {addr[1]}!")
                else:
                    receiver = ("localhost", int(message.decode()[0:4]))
                    server.sendto(message, receiver)
            except:
                pass


t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=send)

t1.start()
t2.start()
