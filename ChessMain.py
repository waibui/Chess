"""
This is our main driver file. It will be responsible for handling user input and displaying the current GameState object.
"""

import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    """
    Initialize a global dictionary of images. This will be called exactly once in the main
    """
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load("assets/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE)
        )

def main():
    """
    The main driver for our code. This will handle user input and updating the graphics
    """
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImages()
    running = True
    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()
        
def drawGameState(screen, gs):
    """
    Responsible for all the graphics within current game state.
    
    Args:
        screen (_pygame.Surface_): The pygame surface to draw on
        gs (GameState): The current game state
    """
    drawBoard(screen)
    drawPieces(screen, gs.board)
    
def drawBoard(screen):
    """
    Draw the squares on the board.

    Args:
        screen (_pygame.Surface_): The pygame surface to draw on
    """
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((c + r) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    """_
    Draw the pieces on the board.

    Args:
        screen (_pygame.Surface_): The pygame surface to draw on
        board (_ChessEngine.GameState_): The current game state
    """
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        
if __name__ == "__main__":
    main()