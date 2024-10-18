import threading
import customtkinter as ctk
import socket
import json
import random
from Console import print_c

SERVER_ADDRESS = "localhost"
SERVER_PORT = 4953

class Server(ctk.CTk):
    def __init__(self):
        
        super().__init__()
        
        self.server_on = False
        self.server_accept = False
        self.server_ban_mode = False
        self.sock = None
        
        self.server_address = SERVER_ADDRESS
        self.server_port = SERVER_PORT
        self.initializeGui()
        self.initializeSocket()
        
        self.users = {}
        self.rooms = {}
        
        self.protocol("WM_DELETE_WINDOW", self.onWindowClose)

    def initializeGui(self) -> None:
        """Initialize the GUI layout and configure widgets"""
        self.title('Chess Server')
        self.geometry("1100x580")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.createSidebar()
        self.createChatbox()
        self.createEntryAndButton()
        self.createUserList()
        self.createFeatureButtons()
        
    def initializeSocket(self) -> None:
        """Initialize server socket and set callback for client connections"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((self.server_address, self.server_port))
            self.sock.listen(5)
            self.running = True
            handler_client_connect = threading.Thread(target=self.handlerClientConnect, daemon=True)
            handler_client_connect.start()
            self.appendMessageSafe(f"[+] Server started at {self.server_address}:{self.server_port}")
            print_c.success(f"Server started at {self.server_address}:{self.server_port}")
        except Exception as e:
            print_c.error(f"Error starting server: {e}")
            
    def handlerClientConnect(self) -> None:
        """Handler for incoming client connections"""
        while self.running:
            try:
                client_socket, client_address = self.sock.accept()
                handle_client_thread = threading.Thread(target=self.handlerClient, args=(client_socket, client_address), daemon=True)
                handle_client_thread.start()  
                self.appendMessageSafe(f"[+] {client_address} connected")
                print_c.success(f"Connected to {client_address}")
            except Exception as e:
                print_c.error(f"Error accepting client: {e}")

    def handlerClient(self, client_socket: socket, client_address: tuple) -> None:
        """Handler for accepted client connections."""
        if client_socket not in self.users:
            self.users[client_socket] = client_address
            self.addUserToList(client_address)
            print_c.success(f"Added {client_address} to user list")
        while self.running:
            try:
                data = client_socket.recv(1024)
                if not data:
                    continue
                message = json.loads(data.decode())

                signal = message.get('signal')
                data = message.get('data')

                if signal == 'join':
                    pass
                    username = data

                elif signal == 'new':
                    random_room = None
                    while True:
                        random_room = random.randint(100000, 999999) 
                        if random_room not in self.rooms: 
                            self.rooms[random_room] = client_socket
                            self.appendMessageSafe(f"[+] Room {random_room} created by {client_address}")
                            client_socket.send(json.dumps({'signal': 'new', 'data': random_room}).encode())
                            print_c.success(f"Room {random_room} created by {client_address}")
                            break 

                elif signal == 'quit':
                    pass
            except Exception as e:
                print_c.error(f"Error in client handler: {e}")
                break

        
    def createSidebar(self) -> None:
        """Create the sidebar panel with control options"""
        self.sidebar = ctk.CTkFrame(self, width=140)
        self.sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar.grid_rowconfigure(8, weight=1)

        self.logo = ctk.CTkLabel(self.sidebar, text="ChessServer", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo.grid(row=0, padx=20, pady=(20, 10))
        
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar, values=["Light", "Dark", "System"], command=self.onAppearanceModeChange)
        self.appearance_mode_optionemenu.grid(row=9, padx=20, pady=(10, 10))
        self.appearance_mode_optionemenu.set("System")

        self.scaling_optionemenu = ctk.CTkOptionMenu(self.sidebar, values=["80%", "90%", "100%", "110%", "120%"], command=self.onScalingChange)
        self.scaling_optionemenu.grid(row=10, padx=20, pady=(10, 20))
        self.scaling_optionemenu.set("100%")

    def createChatbox(self) -> None:
        """Create the chatbox to display messages"""
        self.chatbox_message = ctk.CTkTextbox(self, width=210)
        self.chatbox_message.grid(row=0, column=1, rowspan=3, padx=20, pady=(20, 0), sticky="nsew")
        self.chatbox_message.configure(state="disabled")

    def createEntryAndButton(self) -> None:
        """Create the input entry and send button"""
        self.entry = ctk.CTkEntry(self, placeholder_text="Enter message")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.entry_button = ctk.CTkButton(self, text="Send", fg_color="transparent", border_width=2, command=self.onMessageSend)
        self.entry_button.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def createUserList(self) -> None:
        """Create the list box to show connected users"""
        self.list_box = ctk.CTkScrollableFrame(self, label_text="Users")
        self.list_box.grid(row=0, column=2, rowspan=3, padx=20, pady=(20, 0), sticky="nsew")
        self.list_box.columnconfigure(0, weight=1)

    def createFeatureButtons(self) -> None:
        """Create additional feature buttons"""
        self.feature_buttons_frame = ctk.CTkFrame(self, corner_radius=0)
        self.feature_buttons_frame.grid(row=0, column=3, rowspan=3, padx=(0, 20), pady=(20, 0), sticky="nsew")

        self.label_button_feature = ctk.CTkLabel(self.feature_buttons_frame, text="Feature")
        self.label_button_feature.grid(row=0, column=2, padx=(20, 20), pady=(5, 0), sticky="nsew")

        self.ban_user_entry = ctk.CTkEntry(self.feature_buttons_frame, placeholder_text="User to ban")
        self.ban_user_entry.grid(row=1, column=2, padx=(20, 20), pady=(10, 10), sticky="nsew")

        self.ban_button = ctk.CTkButton(self.feature_buttons_frame, text="Ban User", command=self.onBanUser)
        self.ban_button.grid(row=2, column=2, padx=(20, 20), pady=(10, 20), sticky="nsew")

    def onAppearanceModeChange(self, new_appearance_mode: str) -> None:
        ctk.set_appearance_mode(new_appearance_mode)

    def onScalingChange(self, new_scaling: str) -> None:
        ctk.set_widget_scaling(int(new_scaling.replace("%", "")) / 100)

    def appendMessage(self, message: str) -> None:
        self.chatbox_message.configure(state="normal")
        self.chatbox_message.insert(ctk.END, message + "\n")
        self.chatbox_message.configure(state="disabled")

    def appendMessageSafe(self, message: str) -> None:
        self.after(0, self.appendMessage, message)

    def onClientConnect(self, address, client_socket) -> None:
        """Handle a new client connection and display in the chatbox"""
        pass
    
    def addUserToList(self, username: str) -> None:
        """Add a new user to the user list"""
        button = ctk.CTkButton(self.list_box, text=username, command=lambda: self.removeUserFromList(username))
        button.grid(row=len(self.list_box.grid_slaves()), column=0, padx=10, pady=10, sticky="nsew")

    def removeUserFromList(self, username) -> None:
        """Remove a user from the user list"""
        pass

    def toggleAccept(self) -> None:
        """Toggle accepting new connections"""
        if not self.server_accept:
            self.server_accept = True
            self.appendMessageSafe("[+] Accepting new connections")
            print_c.info("Accepting new connections")
        else:
            self.server_accept = False
            self.appendMessageSafe("[-] Rejecting new connections")
            print_c.info("Rejecting new connections")
            
    def toggleBanMode(self) -> None:
        """Toggle ban mode"""
        pass

    def onBanUser(self) -> None:
        """Ban a user from the server"""
        pass

    def onMessageSend(self) -> None:
        """Send a message to all connected users"""
        pass

    def onWindowClose(self) -> None:
        """Handle window close event"""
        if self.server_on:
            self.sock.off()
            self.sock.join()
        self.destroy()

if __name__ == "__main__":
    server = Server()
    server.mainloop()
