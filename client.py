import socket
import threading



def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))
    running = threading.Event() # shared flag between threads
    running.set()

    def receive_messages():
        while True:
            try:
                message = client.recv(1024).decode()
                print(f"Received: {message}")
                if message == ":q":
                    running.clear()
            except:
                break
    
    threading.Thread(target=receive_messages,
                      daemon=True).start()

    while running.is_set():
        message = input("Message: ")
        client.send(message.encode())

