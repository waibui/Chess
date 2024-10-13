import pygame as p
import pygame_menu
import ChessEngine
from ChessMenu import Menu
from ChessSocket import ClientSocket
import sys

class ChessGame:
    def __init__(self, server_ip='localhost', server_port=4953):
        p.init()
        self.WIDTH = self.HEIGHT = 512
        self.DIMENSION = 8
        self.SQ_SIZE = self.HEIGHT // self.DIMENSION
        self.MAX_FPS = 15
        self.IMAGES = {}
        self.SERVER_IP = server_ip
        self.SERVER_PORT = server_port
        self.screen = p.display.set_mode((self.WIDTH, self.HEIGHT))
        p.display.set_caption('Chess Game')
        self.clock = p.time.Clock()
        self.sock = None

        self.loadImages()
        self.menu_manager = MenuManager(self)
        self.socket_manager = SocketManager(self)

    def loadImages(self):
        """Load the images for the chess pieces."""
        pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
        for piece in pieces:
            self.IMAGES[piece] = p.transform.scale(
                p.image.load(f"assets/images/game/{piece}.png"), (self.SQ_SIZE, self.SQ_SIZE)
            )

    def start(self):
        """Start the game by showing the menu."""
        self.menu_manager.show_main_menu()

    def play_game(self):
        """Main game loop."""
        gs = ChessEngine.GameState()
        valid_moves = gs.getValidMoves()
        move_made = False
        running = True
        sq_selected = ()
        player_clicks = []

        while running:
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                elif e.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos()
                    column = location[0] // self.SQ_SIZE
                    row = location[1] // self.SQ_SIZE
                    if sq_selected == (row, column):
                        sq_selected = ()
                        player_clicks = []
                    else:
                        sq_selected = (row, column)
                        player_clicks.append(sq_selected)
                    if len(player_clicks) == 2:
                        move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                        if move in valid_moves:
                            gs.makeMove(move)
                            move_made = True
                            sq_selected = ()
                            player_clicks = []
                        else:
                            player_clicks = [sq_selected]

                elif e.type == p.KEYDOWN:
                    if e.key == p.K_z:
                        gs.undoMove()
                        move_made = True

            if move_made:
                valid_moves = gs.getValidMoves()
                move_made = False

            self.draw_game_state(gs, sq_selected)
            self.clock.tick(self.MAX_FPS)
            p.display.flip()

        self.quit_game()

    def draw_game_state(self, gs, sq_selected):
        """Draw the current game state."""
        self.draw_board(gs, sq_selected)
        self.draw_pieces(gs.board)

    def draw_board(self, gs, sq_selected):
        """Draw the chessboard."""
        colors = [p.Color("white"), p.Color("gray")]
        in_check = gs.inCheck()
        for r in range(self.DIMENSION):
            for c in range(self.DIMENSION):
                color = colors[(r + c) % 2]
                if sq_selected == (r, c):
                    color = p.Color("#ECDFCC")  # Highlight selected square
                if in_check:
                    if gs.whiteToMove and (r, c) == gs.whiteKingLocation:
                        color = p.Color("red")
                    elif not gs.whiteToMove and (r, c) == gs.blackKingLocation:
                        color = p.Color("red")
                p.draw.rect(self.screen, color, p.Rect(c * self.SQ_SIZE, r * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))

    def draw_pieces(self, board):
        """Draw the chess pieces on the board."""
        for r in range(self.DIMENSION):
            for c in range(self.DIMENSION):
                piece = board[r][c]
                if piece != "--":
                    self.screen.blit(self.IMAGES[piece], p.Rect(c * self.SQ_SIZE, r * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))

    def quit_game(self):
        """Quit the game."""
        p.quit()
        sys.exit()

class MenuManager:
    def __init__(self, game):
        self.game = game

    def show_main_menu(self):
        """Create and display the main menu."""
        main_menu = Menu(title='Chess', width=self.game.WIDTH, height=self.game.HEIGHT, options={
            'buttons': {
                'Play': self.game.play_game,
                'Settings': self.show_settings_menu,
                'Quit': pygame_menu.events.EXIT
            }
        })
        main_menu.mainloop(self.game.screen)

    def show_settings_menu(self):
        """Create and display the settings menu."""
        setting_menu = Menu(title='Settings', width=self.game.WIDTH, height=self.game.HEIGHT, options={
            'inputs': {
                'Server IP': self.game.SERVER_IP,
                'Server Port': self.game.SERVER_PORT
            },
            'buttons': {
                'Apply': pygame_menu.events.EXIT
            }
        })
        return setting_menu
    
class SocketManager:
    def __init__(self, game):
        self.game = game
        self.sock = None

    def connect(self):
        """Create the socket and connect to the server."""
        self.sock = ClientSocket()
        self.sock.start()
        self.sock.connect(self.game.SERVER_IP, self.game.SERVER_PORT)
        self.sock.send_message("wai_bui")

if __name__ == '__main__':
    game = ChessGame()
    game.start()