import sys
import struct
import time
import threading
import socket
import pygame

class TicTacToe:
    def __init__(self, host='127.0.0.1', port=9999):

        self.host = host
        self.port = port

        self.kill = False

        self.socket = None

        self.null_char = 'n'
        self.board = [self.null_char] * 9

        self.turn = 0

        pygame.init()
        self.screen = pygame.display.set_mode((800, 850))
        self.clock = pygame.time.Clock()

        self.space_size = 250
        self.board_center = (self.screen.get_width() / 2, self.screen.get_height() - self.screen.get_width() / 2)
        self.winner = None
        self.teams = ['x', 'o']

        self.clicked = False

        self.font = pygame.font.Font(size=34)

    def draw_letter(self, letter, pos):
        if letter == self.teams[0]:
            pygame.draw.line(self.screen, (0, 0, 255),
                             (pos[0] - self.space_size * 0.4, pos[1] - self.space_size * 0.4),
                             (pos[0] + self.space_size * 0.4, pos[1] + self.space_size * 0.4), 10)
            pygame.draw.line(self.screen, (0, 0, 255),
                             (pos[0] + self.space_size * 0.4, pos[1] - self.space_size * 0.4),
                             (pos[0] - self.space_size * 0.4, pos[1] + self.space_size * 0.4), 10)
        if letter == self.teams[1]:
            pygame.draw.circle(self.screen, (255, 0, 0), pos, self.space_size * 0.4, 10)

    def draw_board(self):
        pygame.draw.line(self.screen, (0, 0, 0),
                         (self.board_center[0] - self.space_size / 2, self.board_center[1] - self.space_size * 1.5),
                         (self.board_center[0] - self.space_size / 2, self.board_center[1] + self.space_size * 1.5))
        pygame.draw.line(self.screen, (0, 0, 0),
                         (self.board_center[0] + self.space_size / 2, self.board_center[1] - self.space_size * 1.5),
                         (self.board_center[0] + self.space_size / 2, self.board_center[1] + self.space_size * 1.5))
        pygame.draw.line(self.screen, (0, 0, 0),
                         (self.board_center[0] - self.space_size * 1.5, self.board_center[1] - self.space_size / 2),
                         (self.board_center[0] + self.space_size * 1.5, self.board_center[1] - self.space_size / 2))
        pygame.draw.line(self.screen, (0, 0, 0),
                         (self.board_center[0] - self.space_size * 1.5, self.board_center[1] + self.space_size / 2),
                         (self.board_center[0] + self.space_size * 1.5, self.board_center[1] + self.space_size / 2))
        
    def place(self, space_index):
        if self.socket:
            self.socket.sendall(struct.pack('B', space_index))

    def get_space(self, pos):
        space_index = pos[0] + pos[1] * 3
        if (0 <= pos[0] < 3) and (0 <= pos[1] < 3):
            return self.board[space_index]

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
    
    def update(self):
        self.screen.fill((255, 255, 255))

        self.clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.kill = True
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clicked = True
        
        mouse_pos = pygame.mouse.get_pos()

        game_text = f'{self.teams[self.turn % 2]}\'s turn'
        if self.winner:
            game_text = f'{self.winner} wins!'
        self.screen.blit(self.font.render(game_text, True, (0, 0, 0)), (10, 10))

        self.draw_board()
        for i, letter in enumerate(self.board):
            space_id = (i % 3, i // 3)
            space_center = ((space_id[0] - 1) * self.space_size + self.board_center[0], (space_id[1] - 1) * self.space_size + self.board_center[1])
            space_r = pygame.Rect(space_center[0] - self.space_size / 2, space_center[1] - self.space_size / 2, self.space_size, self.space_size)
            if letter != self.null_char:
                self.draw_letter(letter, space_center)
            if not self.winner:
                if space_r.collidepoint(mouse_pos):
                    if self.clicked:
                        self.place(i)
        
        self.winner = self.check_win()
            
        pygame.display.update()

        self.clock.tick()

    def deserialize(self, data):
        update_format = 'BB9s'
        # make sure we have enough data in the packet received
        #   note: multiple packets can be bundled or split up
        #   note: if not enough data, should make send data to a buffer until enough is received
        if len(data) >= struct.calcsize(update_format):
            turn, winner, board = struct.unpack_from(update_format, data, 0)
        #   turn: int, winner: int, board: bytes()
            self.turn = turn
        #   chr(): convert ASCII back to char
            if chr(winner) != self.null_char:
                self.winner = chr(winner)
            else:
                self.winner = None 
        #   decode binary into 9 char string, then turn into list of 9 chars
            self.board = list(board.decode('utf-8')) 

    def run_listener(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            s.connect((self.host, self.port))
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True) # lets all packets be processed asap, by default TCP bundles packets before processing
            s.settimeout(1)
            print("Connected: ", s)
            self.socket = s
            while not self.kill:
                try:
                    data = self.socket.recv(4096)
                    if len(data):
                        self.deserialize(data) # convert binary data to usable info
                except socket.timeout:
                    pass
                time.sleep(0.001)
            

    def run(self):
        threading.Thread(target=self.run_listener).start()
        while True:
            self.update()
            time.sleep(0.001)

TicTacToe().run()
