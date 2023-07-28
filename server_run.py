import socket
import threading
import json

clients = {}  # To store client sockets and their nicknames

def handle_client(client_socket):
    nickname = client_socket.recv(1024).decode('utf-8')
    clients[client_socket] = nickname
    send_custom_message(client_socket)
    
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break
        print(f"Received from {nickname}: {data}")
        broadcast(f"[{nickname}] {data}")

    # Remove the client from the clients dictionary when disconnected
    del clients[client_socket]
    client_socket.close()

def broadcast(message):
    for client_socket in clients:
        client_socket.send(message.encode('utf-8'))

def send_custom_message(client_socket):
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)
        custom_message = config_data.get('custom_message', 'Welcome to the chat!')
        client_socket.send(custom_message.encode('utf-8'))

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9999))
    server_socket.listen(5)
    print("Server listening on port 9999...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
