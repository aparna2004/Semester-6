import socket
import threading

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # 3x3 board
        self.current_player = 'X'  # Player X starts

    def print_board(self):
        print(f"{self.board[0]} | {self.board[1]} | {self.board[2]}")
        print("--|---|--")
        print(f"{self.board[3]} | {self.board[4]} | {self.board[5]}")
        print("--|---|--")
        print(f"{self.board[6]} | {self.board[7]} | {self.board[8]}")

    def make_move(self, position):
        if self.board[position] == ' ':
            self.board[position] = self.current_player
            return True
        return False

    def check_winner(self):
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)              # Diagonals
        ]
        for a, b, c in winning_combinations:
            if self.board[a] == self.board[b] == self.board[c] != ' ':
                return True
        return False

    def is_full(self):
        return ' ' not in self.board


def handle_client(player_socket1, player_socket2):
    game = TicTacToe()
    player_sockets = [player_socket1, player_socket2]
    
    while True:
        for player_socket in player_sockets:
            player_socket.sendall(f"Current Board: {game.board}\n".encode())
            if game.is_full():
                for sock in player_sockets:
                    sock.sendall("It's a draw!\n".encode())
                return
            
            position = int(player_socket.recv(1024).decode()) - 1
            
            if game.make_move(position):
                if game.check_winner():
                    player_socket.sendall("You win!\n".encode())
                    other_player = player_sockets[1] if player_socket == player_sockets[0] else player_sockets[0]
                    other_player.sendall("You lose!\n".encode())
                    return
                else:
                    game.current_player = 'O' if game.current_player == 'X' else 'X'
            else:
                player_socket.sendall("Invalid move. Try again.\n".encode())

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen()

    print("Server started. Waiting for players...")
    
    while True:
        player_socket1, addr1 = server_socket.accept()
        print(f"Player 1 connected from {addr1}")
        
        player_socket2, addr2 = server_socket.accept()
        print(f"Player 2 connected from {addr2}")

        threading.Thread(target=handle_client, args=(player_socket1, player_socket2)).start()

if __name__ == "__main__":
    start_server()
