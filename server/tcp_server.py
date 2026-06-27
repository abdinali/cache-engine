import socket
import threading
from cache.lru_cache import LRUCache
from server.protocol import handle_command
from server.responses import BYE

class CacheTCPServer:
    def __init__(self, host, port, max_size):
        self.host = host
        self.port = port
        self.cache = LRUCache(max_size)
        self._lock = threading.Lock()
    
    def start(self):
        # AF_INET = IPv4 internet, SOCK_STREAM = TCP
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen()
        print(f"Listening on {self.host}:{self.port}")

        while True:
            conn, addr = server_socket.accept()
            # create a new thread for per client
            thread = threading.Thread(target=self._handle_client, args=(conn,))
            thread.start()
    
    def _handle_client(self, conn):
        with conn:
            while True:
                # receive and decode from client
                data = conn.recv(1024).decode()
                # empty data means the client disconnected
                if not data:
                    break 
                response = handle_command(self.cache, data.strip(), self._lock)
                # send encoded response
                conn.sendall((response + "\n").encode())
                if response == BYE:
                    break

if __name__ == "__main__":
    server = CacheTCPServer("localhost", 9000, max_size=100)
    server.start()