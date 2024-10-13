import socket
import threading
import time

#### SERVER SOCKET ####
class ServerSocket(threading.Thread):
    def __init__(self, host: str, port: int, callbacks) -> None:
        """Initialize the server socket with a callback for client connections"""
        super().__init__()
        self.host = host
        self.port = port
        self.server_socket = None
        self.accept = False
        self.running = False
        self.clients = {}
        self.callbacks = callbacks
        
    def run(self):
        """Start the server and listen for incoming connections

        Returns:
            super().run()    
        """
        return super().run()

    def on(self) -> None:
        """Start the server and listen for incoming connections"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
        except Exception as e:
            print(f"Error starting server: {e}")

    def acceptClient(self) -> None:
        """Accept incoming client connections"""
        while self.accept:
            try:
                client_socket, address = self.server_socket.accept()
                nickname = client_socket.recv(1024).decode()
                self.appendClient(nickname, client_socket, address)
                handle_client_thread = threading.Thread(target=self.handleClient, args=(client_socket, address), daemon=True)                
                handle_client_thread.start()
            except Exception as e:
                print(f"Error accepting client: {e}")
                
    def appendClient(self, nickname, client_socket, address) -> None:
        """
        Append a client to the list of connected clients
        
        Args:
            nickname (_string_): The nickname of the client
            client_socket (_socket_): The client socket
            address (_tuple_): The address of the client
        """
        if nickname in self.clients:
            self.clients[nickname]["socket"].close()
            del self.clients[nickname]
        else:
            client = {
                        "socket": client_socket,
                        "address": address
                    }
            self.clients[nickname] = client
            self.callbacks['appendMessage'](f"[+]--------[CONNECTED] {nickname} {address[0]}:{address[1]}")    
            self.callbacks['addUserToList'](f"{nickname} {address[0]}")
            
            
            
    def handleClient(self, client_socket, address) -> None:
        """
        Handle communication with a connected client
        
        Args:
            client_socket (_socket_): The client socket
            address (_tuple_): The address of the client
        """
        try:
            while self.running:
                data = client_socket.recv(1024)
                if data:
                    print(f"Received message from {address[0]}:{address[1]}: {data.decode()}")
                else:
                    break
        except Exception as e:
            print(f"Error with client {address}: {e}")
        finally:
            print(f"[-] Client {address[0]}:{address[1]} disconnected")
            client_socket.close()

    def off(self) -> None:
        """Stop the server and close the socket"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
    
#### CLIENT SOCKET ####        
class ClientSocket(threading.Thread):
    def __init__(self) -> None:
        """Initialize the client socket"""
        super().__init__()
        self.client_socket = None
        self.running = False

    def run(self):
        """Start the client and connect to the server"""
        return super().run()

    def connect(self, host: str, port: int) -> None:
        """Connect to the server"""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((host, port))
            print(f"Connected to {host}:{port}")
        except Exception as e:
            print(f"Error connecting to server: {e}")

    def send_message(self, message: str) -> None:
        """Send a message to the server"""
        if self.client_socket:
            self.client_socket.sendall(message.encode())
            print(f"Sent message: {message}")
        else:
            print("Not connected to server")

    def receive_message(self) -> None:
        """Receive a message from the server"""
        if self.client_socket:
            data = self.client_socket.recv(1024)
            if data:
                print(f"Received message: {data.decode()}")
            else:
                print("No data received")
        else:
            print("Not connected to server")
            
    def getSockInfo(self):
        self.host, self.port = self.client_socket.getsockname()
        return self.host, self.port

    def disconnect(self) -> None:
        """Disconnect from the server"""
        if self.client_socket:
            self.client_socket.close()
            print("Disconnected from server")
        else:
            print("Not connected to server")