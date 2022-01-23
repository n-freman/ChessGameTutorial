"""
This class is responsible for storing all the information about the current state of a chess game. It will also be
responsible for determining the valid moves at the current state. It will also keep a move log. 
"""
class GameState:

    def __init__(self):
        # The board is 8x8 2d list, each element of a list has 2 characters.
        # The first character represents the color of the piece, 'b' or 'w'
        # The second character represents the type of the piece, 'K', 'Q', 'R', 'B', 'N' or 'P'
        # "--" represents an empty space with no piece.
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]
        self.white_to_move = True
        self.move_log = []
    
    """
    Takes a Move as a parameter and executes it 
    (this will not work for castling, pawn promotion and en-passant).
    """
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        # Swap players
        self.white_to_move = not self.white_to_move
    
    """
    Undo the last move made.
    """
    def undo_move(self):
        if len(self.move_log) == 0:
            return
        last_move = self.move_log.pop()
        self.board[last_move.start_row][last_move.start_col] = last_move.piece_moved
        self.board[last_move.end_row][last_move.end_col] = last_move.piece_captured
        # Swap players back
        self.white_to_move = not self.white_to_move
        print(f'Undo the move: {last_move.get_chess_notation()}')
    
    """
    All moves considering checks
    """
    def get_valid_moves(self):
        return self.get_all_possible_moves()

    """
    All moves without considering checks
    """
    def get_all_possible_moves(self):
        moves = [Move((6, 4), (4, 4), self.board)]
        # Move((6, 4), (4, 4), self.board)
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == 'w' and self.white_to_move) and (turn=='b' and not self.white_to_move):
                    piece = self.board[row][col][1]
                    if piece == 'P':
                        self.get_pawn_moves(row, col)
                    elif piece == 'R':
                        self.get_rook_moves(row,col)
                    elif piece == 'N':
                        self.get_knight_moves(row, col)
        return moves
    
    """
    Get all the pawn moves for the pawn located at row, col and add these moves to the list.
    """
    def get_pawn_moves(self, row, col, moves):
        pass
    
    """
    Get all the rook moves for the rook located at row, col and add these moves to the list.
    """
    def get_rook_moves(self, row, col, moves):
        pass
        

class Move:
    ranks_to_rows = {
        "1": 7,
        "2": 6,
        "3": 5,
        "4": 4,
        "5": 3,
        "6": 2,
        "7": 1,
        "8": 0,
    }
    row_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {
        "a": 0,
        "b": 1,
        "c": 2,
        "d": 3,
        "e": 4,
        "f": 5,
        "g": 6,
        "h": 7,
    }
    cols_to_files = {v: k for k, v in files_to_cols.items()}


    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
        print(self.move_id)
    
    """
    Overwriting the equals method
    """
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False
    
    def get_chess_notation(self):
        # TODO make a real chess notation
        return self.gat_rank_file(self.start_row, self.start_col) + self.gat_rank_file(self.end_row, self.end_col)
    
    def gat_rank_file(self, row, col):
        return self.cols_to_files[col] + self.row_to_ranks[row]
