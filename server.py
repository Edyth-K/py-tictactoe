import socket
import threading
import json



def run_server():
    # create new socket object for SERVER:
    # parameters: socket type (internet), connection type (TCP)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow port reuse
    
    def receive_from_client(client):  # Add client parameter
        while True:
            try:
                message = client.recv(1024).decode()
                print(f"Client: {message}")
            except:
                break

    try:
        # bind server to address:
        # parameters: a tuple containing (address, port)
        server.bind(('0.0.0.0', 9999))
        # put socket in listening mode
        # can specify amount of connections allowed simultaneously
        server.listen(1)
        print("Server listening on port 9999...")
        
        client, addr = server.accept()
        print(f"Client connected from {addr}")
        
        threading.Thread(target=receive_from_client,
                        args=(client,),
                        daemon=True).start()

        running = True
        while running:

            server_message = input("Server: ")
            client.send(server_message.encode())
            
    except KeyboardInterrupt:
        print("\nServer shutting down gracefully...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up connections
        try:
            client.close()
        except:
            pass  # client might not be defined if error occurred early
        server.close()
        print("Socket closed. Server stopped.")

