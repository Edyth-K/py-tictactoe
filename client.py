import socket

def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))

    while True:

        message = input("Message: ")
        client.send(message.encode())
        print(client.recv(1024).decode())
