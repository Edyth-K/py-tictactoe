import socket
import threading

def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode()
            print(f"Received: {message}")
        except:
            break

def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))
    
    threading.Thread(target=receive_messages,
                      args=(client,),
                      daemon=True).start()

    running = True
    while running:
        message = input("Message: ")
        client.send(message.encode())

