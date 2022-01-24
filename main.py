"""
This is our main driver file. It will be responsible for handling user input 
and displaying the current GameState object.
"""

import pygame as pg
import chess_engine

WIDTH = HEIGHT = 650
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
FPS = 15
square_piece_size_diff = 8
IMAGES = {}


"""
Initialize a global dictionary of images. This will be called exactly once in the main.
"""
def load_images():
    pieces = ['wR', 'wN', 'wB', 'wQ', 'wK', 'wP', 'bR', 'bN', 'bB', 'bQ', 'bK', 'bP']
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(
            pg.image.load(f"Assets/{piece}.png"), 
            (SQ_SIZE-square_piece_size_diff, SQ_SIZE-square_piece_size_diff))
    # Note: we can access an image by saying "IMAGES['wP']"


"""
This main driver for our code. This will handle user input and updating the graphics
"""
def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH-2, HEIGHT-2))
    clock = pg.time.Clock()
    screen.fill(pg.Color('white'))
    gs = chess_engine.GameState()
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
            elif event.type == pg.MOUSEBUTTONDOWN:
                location = pg.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sq_selected == (row, col): # the user clickedd the same square twice
                    sq_selected = ()
                    player_clicks = []
                else:
                    sq_selected = (row, col)
                    # We append for both and the second clicks
                    player_clicks.append(sq_selected)
                    # After the second click
                    if len(player_clicks) == 2:
                        move = chess_engine.Move(
                            player_clicks[0], 
                            player_clicks[1], 
                            gs.board)
                        print(move.get_chess_notation())
                        gs.make_move(move)
                        # Resetting user clicks
                        sq_selected = ()
                        player_clicks = []

        draw_game_state(screen, gs)
        clock.tick(FPS)
        pg.display.flip()


"""
Responsible for all the graphics within a current game state.
"""
def draw_game_state(screen, gs):
    # Draws squares on the board
    draw_board(screen) 
    # Space for adding piece highlighting func
    # Or move suggestion
    # 
    # 
    # Draw pieces on top the of those squares
    draw_pieces(screen, gs.board)


"""
Draw the squares on the board. The top left square is always light.
"""
def draw_board(screen):
    colors = [pg.Color(238, 238, 213), pg.Color(125, 148, 93)]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            # ROW + COLUMN of light squares is always even
            # And for dark squares it is odd. That's how I get color of the square
            color = colors[(row+column) % 2]
            pg.draw.rect(
                screen, color, pg.Rect(column*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE)
                )


"""
Draw the pieces on the board using the current GameState.board
"""
def draw_pieces(screen, board):
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