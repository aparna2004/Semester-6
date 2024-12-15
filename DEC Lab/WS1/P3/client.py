import socket
import sys

def start_client(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    while True:
        board_state = client_socket.recv(1024).decode()
        print(board_state)
        
        if "win" in board_state or "draw" in board_state:
            break
        
        move = input("Enter your move (1-9): ")
        client_socket.sendall(move.encode())

    client_socket.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 client.py <Server_IP> <Port_Number>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    
    start_client(server_ip, server_port)
