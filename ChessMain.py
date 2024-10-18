import pygame as p
import ChessEngine
from Console import print_c
import socket
import threading
import json
import sys

class ChessGame:
    def __init__(self, server_ip='localhost', server_port=4953):
        p.init()
        p.display.set_caption('Chess Game')
        self.WIDTH = self.HEIGHT = 512
        self.DIMENSION = 8
        self.SQ_SIZE = self.HEIGHT // self.DIMENSION
        self.MAX_FPS = 15
        self.IMAGES = {}
        self.SERVER_IP = server_ip
        self.SERVER_PORT = server_port
        self.screen = p.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = p.time.Clock()
        self.sock = None
        self.online = False
        self.running = False

        self.loadImages()
        self.start()
        
    def loadImages(self):
        """Load the images for the chess pieces."""
        pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
        for piece in pieces:
            self.IMAGES[piece] = p.transform.scale(
                p.image.load(f"assets/images/game/{piece}.png"), (self.SQ_SIZE, self.SQ_SIZE)
            )

    def start(self):
        """Start the game by showing the menu."""
        self.initializeSocket()
        self.main_menu()
        
    def main_menu(self):
        """Display the main menu."""
        while True:
            self.screen.fill((0, 0, 0))
            self.display_menu_options()
            for e in p.event.get():
                if e.type == p.QUIT:
                    p.quit()
                    sys.exit()
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_1:  # Play
                        self.play_game()
                    elif e.key == p.K_2:  # Play Online
                        self.join_game()
                    elif e.key == p.K_3:  # New Game
                        self.new_game()
                    elif e.key == p.K_4:  # Quit
                        p.quit()
                        sys.exit()
            p.display.flip()

    def display_menu_options(self):
        """Render the menu options on the screen."""
        font = p.font.Font(None, 36)
        title_surface = font.render('Main Menu', True, (255, 255, 255))
        self.screen.blit(title_surface, (self.WIDTH // 2 - title_surface.get_width() // 2, 50))
        
        options = [
            "1. Play",
            "2. Play Online",
            "3. New Game",
            "4. Quit"
        ]
        
        for i, option in enumerate(options):
            option_surface = font.render(option, True, (255, 255, 255))
            self.screen.blit(option_surface, (self.WIDTH // 2 - option_surface.get_width() // 2, 100 + i * 40))

    def play_game(self, room_number=None):
        """Main game loop."""
        print_c.info('Starting game...')
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
                    color = p.Color("#ECDFCC") 
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
    
    def initializeSocket(self) -> None:
        """Setup the socket."""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.connect((self.SERVER_IP, self.SERVER_PORT))
            self.running = True
            self.handler_server_thread = threading.Thread(target=self.handlerServer, daemon=True)
            self.handler_server_thread.start()
            print_c.success(f"Connected to {self.SERVER_IP}:{self.SERVER_PORT}")
        except Exception as e:
            print_c.error(f"Error connecting to server: {e}")
            
    def handlerServer(self) -> None:
        """Handle server messages."""
        while self.running:
            try:
                data = self.sock.recv(1024)
                if not data:
                    continue
                message = json.loads(data.decode())   
                
                signal = message.get('signal')
                data = message.get('data')
                
                if signal == 'join':
                    room_number = data
                    print_c.success(f"Joined room {room_number}")
                    
                elif signal == 'new':
                    room_number = data
                    self.play_game(room_number=room_number)
                    p.display.set_caption(f"ROOM: {str(room_number)}")
                    print_c.success(f"New room {room_number} created")
                    
            except Exception as e:
                print_c.error(f"Error connecting to server: {e}")        
                break
            
    def send_message(self, message: str, signal: str, to: str = 'server') -> None:
        """Send a message to the server or another player."""
        if self.running:
            message_payload = {
                'signal': signal,
                'data': message,
            }
            
            try:
                self.sock.send(
                    json.dumps(message_payload).encode()
                )
                print_c.message(f"Sent message: {message_payload}")
            except Exception as e:
                print_c.error(f"Error sending message to server: {e}")
        else:
            print("Not connected to server")
        
    def join_game(self) -> None:
        """Join a game by sending a 'join' signal to the server."""
        self.send_message('join', 'join', 'server')
    
    def new_game(self) -> None:
        """Start a new game."""
        self.send_message('new', 'new', 'server')
        
    def quit_game(self) -> None:
        """Quit the game."""
        p.quit()
        sys.exit()

if __name__ == '__main__':
    game = ChessGame()
    game.start()
