"""
This is our main driver file. It will be responsible for handling user input and displaying the current GameState object.
"""

import pygame as pg
import chess_engine

WIDTH = HEIGHT = 650
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
FPS = 15
IMAGES = {}
"""
Initialize a global dictionary of images. This will be called exactly once in the main.
"""
def load_images():
    pieces = ['wR', 'wN', 'wB', 'wQ', 'wK', 'wP', 'bR', 'bN', 'bB', 'bQ', 'bK', 'bP']
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load(f"Assets/{piece}.png"), (SQ_SIZE, SQ_SIZE))
    # Note: we can access an image by saying "IMAGES['wP']"


"""
This main driver for our code. This will handle user input and updating the graphics
"""
def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color('white'))
    gs = chess_engine.GameState()
    load_images()
    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        clock.tick(FPS)
        pg.diplay.flip()


if __name__ == "__main__":
    main()