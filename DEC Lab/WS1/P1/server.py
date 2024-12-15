import socket
import threading

server_ip = '0.0.0.0'
server_port = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen()

clients = []

def handle_client(client_socket, address):
    print(f"Connection from {address} has been established!")
    clients.append(client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(f"{message=}")
            if message:
                broadcast(message, client_socket)
            else:
                break
        except:
            break

    client_socket.close()
    clients.remove(client_socket)
    print(f"Connection from {address} closed.")

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                clients.remove(client)

while True:
    client_socket, address = server_socket.accept()
    threading.Thread(target=handle_client, args=(client_socket, address)).start()

