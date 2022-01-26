"""
This is our main driver file. It will be responsible for handling user input 
and displaying the current GameState object.
"""

import pygame as pg
import chess_engine

WIDTH = HEIGHT = 650
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
EXTRA_SPACE_ON_SCREEN = WIDTH - SQ_SIZE * DIMENSION
FPS = 15
square_piece_size_diff = 0
IMAGES = {}


def load_images():
    """
    Initialize a global dictionary of images. This will be called exactly once in the main.
    """
    pieces = ['wR', 'wN', 'wB', 'wQ', 'wK', 'wP', 'bR', 'bN', 'bB', 'bQ', 'bK', 'bP']
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(
            pg.image.load(f"Assets/{piece}.png"), 
            (SQ_SIZE-square_piece_size_diff, SQ_SIZE-square_piece_size_diff))
    # Note: we can access an image by saying "IMAGES['wP']"


def main():
    """
    This main driver for our code. This will handle user input and updating the graphics
    """
    pg.init()
    screen = pg.display.set_mode(
        (WIDTH-EXTRA_SPACE_ON_SCREEN, 
        HEIGHT-EXTRA_SPACE_ON_SCREEN)
        )
    clock = pg.time.Clock()
    # screen.fill(pg.Color('white'))
    gs = chess_engine.GameState()
    valid_moves = gs.get_valid_moves()
    # move_mode is a flag variabla for when a move is made.
    move_made = False
    load_images()
    running = True
    # The sq_selected variable is for keeping track of last clicked square => tuple(row, col).
    sq_selected = ()
    # The player_clicks is for keeping tracks of clicks (two tuples => [(6, 4), (4, 4)])
    player_clicks = []

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            # Mouse press handler
            elif event.type == pg.MOUSEBUTTONDOWN:
                location = pg.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sq_selected == (row, col): # the user clickedd the same square twice
                    sq_selected = ()
                    player_clicks = []
                else:
                    sq_selected = (row, col)
                    # pg.draw.rect(
                    # screen, pg.Color(255, 240, 200,  50), pg.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE)
                    # )
                    # pg.display.flip()
                    # We append for both and the second clicks
                    player_clicks.append(sq_selected)
                    # After the second click
                    if len(player_clicks) == 2:
                        move = chess_engine.Move(
                            player_clicks[0], 
                            player_clicks[1], 
                            gs.board)
                        
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                gs.make_move(valid_moves[i])
                                print(move.get_chess_notation())
                                move_made = True
                                # Resetting user clicks
                                sq_selected = ()
                                player_clicks = []
                        if not move_made:
                            player_clicks = [sq_selected]
            # Keyboard handler
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_c:
                    gs.undo_move()
                    move_made = True

        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False

        draw_game_state(screen, gs, sq_selected, valid_moves)
        clock.tick(FPS)
        pg.display.flip()


def draw_game_state(screen, gs, sq_selected, moves):
    """
    Responsible for all the graphics within a current game state.
    """
    # Draw squares on the board
    draw_board(screen, sq_selected) 
    # Space for adding piece highlighting func
    # Or move suggestion
    draw_movable_squares(screen, sq_selected, moves)
    # 
    # Draw pieces on top the of those squares
    draw_pieces(screen, gs.board)


def draw_board(screen, sq_selected):
    """
    Draw the squares on the board. The top left square is always light.
    """
    colors = [pg.Color('#fafafa'), pg.Color('#868786')]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            # ROW + COLUMN of light squares is always even
            # And for dark squares it is odd. That's how to get color of the square
            color = colors[(row+column) % 2]
            pg.draw.rect(
                screen, color, pg.Rect(column*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE)
                )
            if sq_selected != ():
                if (row, column) == sq_selected:
                    pg.draw.rect(
                    screen, pg.Color(255, 243, 95), pg.Rect(column*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE)
                    )


def draw_movable_squares(screen, sq_selected, moves):
    for move in moves:
                if sq_selected != ():
                    if ((move.start_row, move.start_col) == sq_selected):
                        pg.draw.circle(screen, pg.Color('#666564'), (move.end_col*SQ_SIZE+SQ_SIZE/2, move.end_row*SQ_SIZE+SQ_SIZE/2), 10, 10)
            


def draw_pieces(screen, board):
    """
    Draw the pieces on the board using the current GameState.board
    """
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != '--':
                # We aded half of square_piece_size_diff to the piece position to make it on the centre of the square
                half_diff = square_piece_size_diff/2
                screen.blit(
                    IMAGES[piece], pg.Rect(
                        column*SQ_SIZE+half_diff, 
                        row*SQ_SIZE+half_diff, 
                        SQ_SIZE, 
                        SQ_SIZE)
                    )


if __name__ == "__main__":
    main()
