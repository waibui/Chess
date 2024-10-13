import threading
import customtkinter as ctk
from ChessSocket import ServerSocket

SERVER_ADDRESS = "localhost"
SERVER_PORT = 4953

class Server(ctk.CTk):
    def __init__(self):
        
        super().__init__()
        
        self.server_on = False
        self.server_accept = False
        self.server_ban_mode = False
        
        self.callbacks = {
            "appendMessage": self.appendMessageSafe,
            "addUserToList": self.addUserToList,
            "removeUserFromList": self.removeUserFromList
        }
        
        self.initializeGui()
        self.server_address = SERVER_ADDRESS
        self.server_port = SERVER_PORT
        self.initializeSocket()
        
        self.users = {}
        
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

    def createSidebar(self) -> None:
        """Create the sidebar panel with control options"""
        self.sidebar = ctk.CTkFrame(self, width=140)
        self.sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar.grid_rowconfigure(8, weight=1)

        self.logo = ctk.CTkLabel(self.sidebar, text="ChessServer", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo.grid(row=0, padx=20, pady=(20, 10))

        self.btn_start = ctk.CTkSwitch(self.sidebar, text="Start Server", command=self.toggleServer)
        self.btn_start.grid(row=1, padx=20, pady=10)

        self.btn_accept = ctk.CTkSwitch(self.sidebar, text="Accept Connection", command=self.toggleAccept)
        self.btn_accept.grid(row=2, padx=20, pady=10)

        self.btn_ban = ctk.CTkSwitch(self.sidebar, text="Ban Mode", command=self.toggleBanMode)
        self.btn_ban.grid(row=3, padx=20, pady=10)

        self.address = ctk.CTkLabel(self.sidebar, text="Address")
        self.address.grid(row=4, padx=20, pady=(10, 0))
        self.entry_address = ctk.CTkEntry(self.sidebar, placeholder_text="localhost")
        self.entry_address.grid(row=5, padx=20, pady=(10, 0))

        self.port = ctk.CTkLabel(self.sidebar, text="Port")
        self.port.grid(row=6, padx=20, pady=(10, 0))
        self.entry_port = ctk.CTkEntry(self.sidebar, placeholder_text="4953")
        self.entry_port.grid(row=7, padx=20, pady=(10, 0))

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

    def initializeSocket(self) -> None:
        """Initialize server socket and set callback for client connections"""
        self.sock = ServerSocket(self.server_address, self.server_port, self.callbacks)
        self.sock.start()
    
    def onClientConnect(self, address, client_socket) -> None:
        """Handle a new client connection and display in the chatbox"""
        self.appendMessageSafe(f"[-] client {address[0]}:{address[1]} connected")
        if self.server_on:
            pass
    
    def addUserToList(self, username: str) -> None:
        """Add a new user to the user list"""
        button = ctk.CTkButton(self.list_box, text=username, command=lambda: self.removeUserFromList(username))
        button.grid(row=len(self.list_box.grid_slaves()), column=0, padx=10, pady=10, sticky="nsew")

    def removeUserFromList(self, username) -> None:
        """Remove a user from the user list"""
        pass

    def toggleServer(self) -> None:
        """Start or stop the server"""
        self.server_address = self.entry_address.get().strip() if self.entry_address.get().strip() else self.server_address
        self.server_port = self.entry_port.get().strip() if self.entry_port.get().strip() else self.server_port
        if self.server_on:
            self.sock.off()
            self.server_on = False
            self.appendMessageSafe("[-] server stopped")
        else:
            self.sock.on()
            self.server_on = True
            self.appendMessageSafe("[+] server started")
            
    def toggleAccept(self) -> None:
        """Toggle accepting new connections"""
        if self.server_accept:
            self.server_accept = False
            self.sock.accept = False
            self.appendMessageSafe("[-] disabled accept")
        else:
            self.accept_thread = threading.Thread(target=self.sock.acceptClient, daemon=True)
            self.sock.accept = True
            self.server_accept = True
            self.accept_thread.start()
            self.appendMessageSafe("[+] enabled accept")
            
    def toggleBanMode(self) -> None:
        """Toggle ban mode"""
        pass

    def onBanUser(self) -> None:
        """Ban a user from the server"""
        pass

    def onMessageSend(self) -> None:
        """Send a message to all connected users"""
        message = self.entry.get().strip()
        if message:
            self.appendMessageSafe(f"[Server]: {message}")
            with self.list_user_lock:
                for username, client_socket in self.list_user.items():
                    if username not in self.banned_users:
                        try:
                            client_socket.sendall(message.encode())
                        except Exception as e:
                            print(f"[-] Failed to send message to {username}: {e}")

    def onWindowClose(self) -> None:
        """Handle window close event"""
        if self.server_on:
            self.sock.off()
            self.sock.join()
        self.destroy()

if __name__ == "__main__":
    server = Server()
    server.mainloop()
