import sqlite3
import chess

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]

    def move(self, position_from, position_to):
        start_row, start_col = position_from
        end_row, end_col = position_to
        piece = self.grid[start_row][start_col]
        if piece is None:
            return False
        if not piece.is_valid_move(position_from, position_to):
            return False
        self.grid[start_row][start_col] = None
        self.grid[end_row][end_col] = piece
        return True

class Piece:
    def __init__(self, color):
        self.color = color

    def is_valid_move(self, position_from, position_to):
        raise NotImplementedError()

class King(Piece):
    def __init__(self, color):
        super().__init__(color)

    def is_valid_move(self, position_from, position_to):
        return True

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)

    def is_valid_move(self, position_from, position_to):
        return True

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)

    def is_valid_move(self, position_from, position_to):
        return True

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)

    def is_valid_move(self, position_from, position_to):
        return True

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)

    def is_valid_move(self, position_from, position_to):
        return True

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)

    def is_valid_move(self, position_from, position_to):
        return True

# Підключення до бази даних SQLite
conn = sqlite3.connect('chess.db', check_same_thread=False)
cursor = conn.cursor()

# Створення таблиці для зберігання стану гри, якщо вона не існує
cursor.execute('''CREATE TABLE IF NOT EXISTS chess_game
              (id INTEGER PRIMARY KEY, fen TEXT)''')
conn.commit()

board = False
fen = False

# Вставлення початкового стану гри в базу даних
cursor.execute('INSERT INTO chess_game (fen) VALUES (?)', (fen,))
conn.commit()

def get_board():
    if is_game_ended():
        print("Board is empty. Plese start a game")
    else: 
        print(str(board))
        return str(board)

def start_game():
    global board
    global fen
    board = chess.Board()
    fen = board.fen()
    print("Game is started")
    get_board()

def move(position_from: str, position_to: str): 
    if is_game_ended():
        print("Game is ended. Plese start new game")
    else:
        try:
            move = chess.Move.from_uci(position_from + position_to)
        except:
            print("Typo in move. Please use e.g. 'e2/e4'")
        if move in board.legal_moves:
            board.push(move)
            fen = board.fen()
            cursor.execute('INSERT INTO chess_game (fen) VALUES (?)', (fen,))
            conn.commit()
            print("Move successful")
            get_board()
        else:
            print("The object can't move in such way")

def end_game():
    if is_game_ended():
        print("Game is already ended")
    else:
        global board
        global fen
        board = None
        fen = None
        print("Game is ended")

def is_game_ended():
    if board == None or board == False:
        return True
    else:
        return board.is_game_over()

while board != None:
    prompt = input('Enter command: ')

    if prompt == 'get_board':
        get_board()
    
    if prompt == 'start_game':
        start_game()

    if prompt == 'move':
        position_from = input('Please enter position from: ')
        position_to = input('Please enter position to: ')
        move(position_from, position_to)
    
    if prompt == 'end_game':
        end_game()

    if prompt == 'is_game_ended':
        print(is_game_ended())