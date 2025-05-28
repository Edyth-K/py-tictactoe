import socket

# create new socket object for SERVER: 
# parameters: socket type (internet), connection type (TCP)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind server to address:
# parameters: a tuple containing (address, port)
server.bind(('0.0.0.0', 9999))

# put socket in listening mode
# can specify amount of connections allowed simultaneously 
server.listen(5)

while True:
    # constantly accept connections
    # server.accept() returns two variables:
        # client: the client instance we use to communicate
        # address: the address of the client
    client, addr = server.accept()

    print(client.recv(1024).decode())
    client.send('Hello From Server'.encode())