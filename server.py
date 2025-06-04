import socket
import threading # for async
import time
import struct # for encoding/decoding of binary data

class Server:
    def __init__(self, host='127.0.0.1', port=9999):
        self.host = host
        self.port = port

        self.kill = False # kill flag for dealing with multi-threaded stuff
        self.thread_count = 0 # lets us know when everything is shut down

        self.null_char = 'n'
        self.board = [self.null_char] * 9

        self.turn = 0
        self.winner = self.null_char
        self.teams = ['x', 'o']

        self.players = []

    # generate all board data in binary
    def serialize(self):
        return struct.pack('BB9s', self.turn, ord(self.winner), ''.join(self.board).encode('utf-8'))
        # BB9s: 2 unsigned char as bytes, followed by 9 byte string     
        # ord() converts single char into ASCII

    def place(self, conn, space_index):
        if self.winner == self.null_char:
            player_id = self.players.index(conn) # this becomes either 0 or 1, to find out which player is sending move
            if 0 <= space_index < len(self.board) and (player_id == (self.turn % 2)):
                if self.board[space_index] == self.null_char:
                    self.board[space_index] = self.teams[player_id]
                    self.turn += 1

    def get_space(self, pos):
        space_index = pos[0] + pos[1] * 3
        if (0 <= pos[0] < 3) and (0 <= pos[1] < 3):
            return self.board[space_index]

    # server validation
    def check_win(self):
        for i, letter in enumerate(self.board):
            if letter != self.null_char:
                space_id = (i % 3, i // 3)
                for angle in [(1, 0), (1, 1), (0, 1), (-1, 1)]:
                    for j in range(3):
                        if self.get_space((space_id[0] + angle[0] * j, space_id[1] + angle[1] * j)) != letter:
                            break
                        if j == 2:
                            return letter
        return self.null_char
    # listener for clients
    def run_listener(self, conn):
        self.thread_count += 1
        conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        conn.settimeout(1)
        with conn:
            while not self.kill:
                # loop to receive data
                try:
                    # receives binary data
                    data = conn.recv(4096)
                    if len(data):
                        target_space = struct.unpack_from('B', data, 0)[0]
                        self.place(conn, target_space)
                except socket.timeout:
                    pass
                except (ConnectionAbortedError, ConnectionResetError):
                    break
        self.thread_count -= 1

    # listener for connections
    def connection_listen_loop(self):
        # this will be its own thread
        
        # start thread
        self.thread_count += 1

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # TCP socket
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True) # optional: easier to reuse address
            s.bind((self.host, self.port)) # listener
            
            while not self.kill:
                s.settimeout(1) # prevents getting stuck in a socket call when trying to stop thread
                s.listen()
                try:
                    conn, addr = s.accept()
                    print("New Connection: ", conn, addr)
                    if len(self.players) < 2:
                        self.players.append(conn)
                        threading.Thread(target=self.run_listener, args=(conn,)).start()
                except socket.timeout:
                    # when no one connects, just move on
                    continue
                time.sleep(0.01)


        # kill thread
        self.thread_count -= 1

    def await_kill(self):
        self.kill = True
        while self.thread_count:
            time.sleep(0.01)
        print("killed")

    def run(self):
        threading.Thread(target=self.connection_listen_loop).start()
        # main loop
        try:
            while True:
                # server action here
                self.winner = self.check_win()
                for player_conn in self.players:
                    try:
                        player_conn.send(self.serialize()) # send board data to client
                    except OSError:
                        pass
                time.sleep(0.05)

        except KeyboardInterrupt:
            self.await_kill()

Server().run()

