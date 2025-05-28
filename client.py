import socket

LOCAL_HOST = '127.0.0.1'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((LOCAL_HOST, 9999))

client.send("hello".encode())
print(client.recv(1024).decode())