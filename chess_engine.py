from tabnanny import check
from turtle import st


class GameState:
    """
    This class is responsible for storing all the information about the current state of a chess game. It will also be
    responsible for determining the valid moves at the current state. It will also keep a move log.
    """

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
        self.move_functions = {
            'P': self.get_pawn_moves,
            'R': self.get_rook_moves,
            'N': self.get_knight_moves,
            'B': self.get_bishop_moves,
            'Q': self.get_queen_moves,
            'K': self.get_king_moves,
        }
        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.pins = []
        self.checks = []
        self.check_mate = False
        self.stale_mate = False
      
    def make_move(self, move):
        """
        Takes a Move as a parameter and executes it 
        (this will not work for castling, pawn promotion and en-passant).
        """
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        # Swap players
        self.white_to_move = not self.white_to_move
        if move.piece_moved == 'wk':
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == 'bK':
            self.black_king_location = (move.end_row, move.end_col)
    
    def undo_move(self):
        """
        Undo the last move made.
        """
        if len(self.move_log) == 0:
            return
        last_move = self.move_log.pop()
        self.board[last_move.start_row][last_move.start_col] = last_move.piece_moved
        self.board[last_move.end_row][last_move.end_col] = last_move.piece_captured
        # Swap players back
        self.white_to_move = not self.white_to_move
        if last_move.piece_moved == 'wk':
            self.white_king_location = (last_move.start_row, last_move.start_col)
        elif last_move.piece_moved == 'bK':
            self.black_king_location = (last_move.start_row, last_move.start_col)
    
    def get_valid_moves(self):
        """
        All moves considering checks
        """
        moves = []
        self.in_check, self.pins, self.checks = self.check_for_pins_and_checks()
        if self.white_to_move:
            king_row = self.white_king_location[0]
            king_col = self.white_king_location[1]
        else:
            king_row = self.black_king_location[0]
            king_col = self.black_king_location[1]
        if self.in_check:
            if len(self.checks) == 1:
                moves = self.get_all_possible_moves()
                check = self.checks[0]
                check_row = check[0]
                check_col = check[1]
                piece_checking = self.board[check_row][check_col]
                valid_squares = []
                if piece_checking[1] == 'N':
                    valid_squares = [(check_row, check_col)]
                else:
                    for i in range(1, 8):
                        valid_square = (king_row + check[2] * i, king_col + check[3] * i)
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col:
                            break
                for i in range(len(moves)-1, -1, -1):
                    if moves[i].piece_moved[1] != 'K':
                        if not (moves[i].end_row, moves[i].end_col) in valid_squares:
                            moves.remove(moves[i])
            else:
                self.get_king_moves(king_row, king_col, moves)
        else:
            moves = self.get_all_possible_moves()
        
        return moves

    def get_all_possible_moves(self):
        """
        All moves without considering checks.
        """
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == 'w' and self.white_to_move) or (turn=='b' and not self.white_to_move):
                    piece = self.board[row][col][1]
                    self.move_functions[piece](row, col, moves)
        return moves
    
    def get_pawn_moves(self, row, col, moves):
        """
        Get all the pawn moves for the pawn located at row, col and add these moves to the list.
        """
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.white_to_move:
            if self.board[row-1][col] == '--':
                if not piece_pinned or pin_direction == (-1, 0):
                    moves.append(Move((row, col), (row-1, col), self.board))
                    if row == 6 and self.board[row-2][col]:
                        moves.append(Move((row, col), (row-2, col), self.board))
            if col - 1 >= 0:
                if self.board[row-1][col-1][0] == 'b':
                    if not piece_pinned or pin_direction == (-1, -1):
                        moves.append(Move((row, col), (row-1, col-1), self.board))
            if col + 1 <= 7:
                if self.board[row-1][col+1][0] == 'b':
                    if not piece_pinned or pin_direction == (-1, 1):
                        moves.append(Move((row, col), (row-1, col+1), self.board))
        else:
            if self.board[row+1][col] == '--':
                if not piece_pinned or pin_direction == (1, 0):
                    moves.append(Move((row, col), (row+1, col), self.board))
                    if row == 1 and self.board[row+2][col] == '--':
                        moves.append(Move((row, col), (row+2, col), self.board))
            if col - 1 >= 0:
                if not piece_pinned or pin_direction == (1, -1):
                    if self.board[row+1][col-1][0] == 'w':
                        moves.append(Move((row, col), (row+1, col-1), self.board))
            if col + 1 <= 7:
                if not piece_pinned or pin_direction == (1, 1):
                    if self.board[row+1][col+1][0] == 'w':
                        moves.append(Move((row, col), (row+1, col+1), self.board))
        # Add pawn promotion later
    
    def get_rook_moves(self, row, col, moves):
        """
        Get all the rook moves for the rook located at row, col and add these moves to the list.
        """
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[row][col][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = row + d[0] * i
                end_col = col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == '--':
                            moves.append(
                                Move(
                                    (row, col), 
                                    (end_row, end_col), 
                                    self.board))
                        elif end_piece[0] == enemy_color:
                            moves.append(
                                Move(
                                    (row, col), 
                                    (end_row, end_col), 
                                    self.board))
                            break
                        else:
                            break
                else:
                    break
    
    def get_knight_moves(self, row, col, moves):
        piece_pinned = False
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        ally_color = 'w' if self.white_to_move else 'b'
        for m in knight_moves:
            end_row = row + m[0]
            end_col = col + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                if not piece_pinned:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] != ally_color:
                        moves.append(
                                Move(
                                    (row, col), 
                                    (end_row, end_col), 
                                    self.board))

    def get_bishop_moves(self, row, col, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = row + d[0] * i
                end_col = col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == '--':
                            moves.append(
                                Move(
                                    (row, col), 
                                    (end_row, end_col), 
                                    self.board))
                        elif end_piece[0] == enemy_color:
                            moves.append(
                                Move(
                                    (row, col), 
                                    (end_row, end_col), 
                                    self.board))
                            break
                        else:
                            break
                else:
                    break
        
    def get_queen_moves(self, row, col, moves):
        self.get_rook_moves(row, col, moves)
        self.get_bishop_moves(row, col, moves)

    def get_king_moves(self, row, col, moves):
        possible_moves = ((1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1))
        ally_color = 'w' if self.white_to_move else 'b'
        for m in possible_moves:
            end_row = row + m[0]
            end_col = col + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    if ally_color == 'w':
                        self.white_king_location = (end_row, end_col)
                    else:
                        self.black_king_location = (end_row, end_col)
                    in_check, pins, checks = self.check_for_pins_and_checks()
                    if not in_check:
                        moves.append(
                            Move(
                                (row, col), 
                                (end_row, end_col), 
                                self.board))
                    if ally_color == 'w':
                        self.white_king_location = (row, col)
                    else:
                        self.black_king_location = (row, col)
    
    def check_for_pins_and_checks(self):
        pins = []
        checks = []
        in_check = False
        if self.white_to_move:
            enemy_color = 'b'
            ally_color = 'w'
            start_row = self.white_king_location[0]
            start_col = self.white_king_location[1]
        else:
            enemy_color = 'w'
            ally_color = 'b'
            start_row = self.black_king_location[0]
            start_col = self.black_king_location[1]
        directions = ((1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1))
        for j in range(len(directions)):
            d = directions[j]
            possible_pin = ()
            for i in range(1, 8):
                end_row = start_row + d[0] * i
                end_col = start_col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_color and end_piece[1] != 'K':
                        if possible_pin == ():
                            possible_pin = (end_row, end_col, d[0], d[1])
                        else:
                            break
                    elif end_piece[0] == enemy_color:
                        type_of_enemy = end_piece[1]
                        # 5 possibilities here in this complex conditional
                        # 1. orthogonally away from king and piece is a rook
                        # 2. diagonally away from king and piece is a bishop
                        # 3. 1 square away diaonally from king and piece is a pawn
                        # 4. any direction and piece is a pawn
                        # 5. any direction 1 square away from king 
                        # Last one is necessary to prevent a king move to a square controlled by another king
                        if (0 <= j <= 3 and type_of_enemy == 'R') or \
                                (4 <= j <= 7 and type_of_enemy == 'B') or \
                                (i == 1 and type_of_enemy == 'P' and \
                                    ((enemy_color == 'w' and 6 <= j <=7) or (enemy_color == 'b' and 4 <= j <= 5))) or \
                                (type_of_enemy == 'Q') or (i == 1 and type_of_enemy == 'K'):
                            if possible_pin == ():
                                in_check = True
                                checks.append((end_row, end_col, d[0], d[1]))
                                break
                            else:
                                pins.append(possible_pin)
                                break
                        else:
                            break
                else:
                    break
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knight_moves:
            end_row = start_row + m[0]
            end_col = start_col + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece[1] == 'N':
                    in_check = True
                    checks.append((end_row, end_col, m[0], m[1]))
        return in_check, pins, checks

    
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

    def __eq__(self, other):
        """
        Overwriting the equals method
        """
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False
    
    def get_chess_notation(self):
        # TODO make a real chess notation
        return self.gat_rank_file(self.start_row, self.start_col) + self.gat_rank_file(self.end_row, self.end_col)
    
    def gat_rank_file(self, row, col):
        return self.cols_to_files[col] + self.row_to_ranks[row]
