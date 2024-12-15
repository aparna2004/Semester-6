import socket
import threading
import sys

def send_messages(client_socket):
    while True:
        message = input("Enter : ")
        print(f"{message=}")
        if message.lower() == "exit":
            break
        client_socket.send(message.encode('utf-8'))

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                break
        except:
            print("An error occurred!")
            break

# Client configuration
server_ip = sys.argv[1]
server_port = int(sys.argv[2])

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

threading.Thread(target=receive_messages, args=(client_socket,)).start()
send_messages(client_socket)

client_socket.close()
