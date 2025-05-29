# game logic and rendering

def render_board(board):
    """
    Draw board to screen
    
    Args:
        board (list): 3x3 list of lists representing the game board
    """

    print ("-------------")
    for row in board:
        print (f"| {row[0]} | {row[1]} | {row[2]} |")
        print ("-------------")

def update_board(board, pos, player):
    """
    Update board state
    
    Args:
        board (list): 3x3 list of lists representing the game board
        pos (int): (1-9) representing where to place o/x
        player (string): "o" or "x" to indicate which to draw

    Returns: 
        board (list): 3x3 list of lists representing updated board
    """
    match pos:
        case 1:
            board[0][0] = player
        case 2:
            board[0][1] = player
        case 3:
            board[0][2] = player
        case 4:
            board[1][0] = player
        case 5:
            board[1][1] = player
        case 6:
            board[1][2] = player
        case 7:
            board[2][0] = player
        case 8:
            board[2][1] = player
        case 9:
            board[2][2] = player
        case _:
            return board
    return board


# remove later
def main():
    board = [
    [' ',' ',' '],
    [' ',' ',' '],
    [' ',' ',' ']
]
    
    print("Welcome to Tic Tac Toe.")
    render_board(board)

    # Game Loop
    while True:
        input_position = input("Enter Position (1-9): ")
        board = update_board(board, int(input_position), "x")
        print(board)
        render_board(board)

if __name__ == "__main__":
    main()