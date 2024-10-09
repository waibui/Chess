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
    validMoves = gs.getValidMoves()
    moveMade = False # Flag variable for when a move is made
    loadImages()
    running = True
    sqSelected = () # no square is selected, keep track of the last click of the user (tuple: (row, col))
    playerClicks = [] # keep track of player clicks (2 tuples: [(6, 4), (4, 4)])
    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                column = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, column):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, column)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = ()
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]

            # key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
            
        drawGameState(screen, gs, sqSelected)
        clock.tick(MAX_FPS)
        p.display.flip()
        
def drawGameState(screen, gs, sqSelected):
    """
    Responsible for all the graphics within current game state.
    
    Args:
        screen (_pygame.Surface_): The pygame surface to draw on
        gs (GameState): The current game state
    """
    drawBoard(screen, gs, sqSelected)
    drawPieces(screen, gs.board)
    
def drawBoard(screen,gs , sqSelected=()):
    """
    Draw the squares on the board.

    Args:
        screen (_pygame.Surface_): The pygame surface to draw on
    """
    colors = [p.Color("white"), p.Color("gray")]
    inCheck = gs.inCheck()

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            if sqSelected == (r, c):
                color = p.Color("#ECDFCC")  # Highlight selected square

            if inCheck:
                if gs.whiteToMove and (r, c) == gs.whiteKingLocation:
                    color = p.Color("red")
                elif not gs.whiteToMove and (r, c) == gs.blackKingLocation:
                    color = p.Color("red")

            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    """_
    Draw the pieces on the board.

    Args:
        screen (_pygame.Surface_): The pygame surface to draw on
        board (_ChessEngine.GameState_): The current game state
    """
    for r in range(DIMENSION): # rows
        for c in range(DIMENSION): # columns
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        
if __name__ == "__main__":
    main()