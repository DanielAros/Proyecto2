import socket
import threading

host = 'LocalHost'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen()
print("Sevidor esperando")

clients = []
usernames = []

def broadcast(message, _client):
    for client in clients:
        if client != _client:
            client.send(message)

def handle_messages (client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except:
            index = clients.index(client)
            username = usernames [index]
            broadcast(f"chatbot: {username} disconected".encode('utf-8'))
            clients.remove(client)
            username.remove(username)
            client.close()
            break
def receive_connections():
    while True:
        client, address = server.accept()
        client.send("@username".encode('utf-8'))
        username = client.recv(1024).decode('utf-8')

        clients.append(client)
        usernames.append(username)

        print(f"{username} esta conectado {str(address)}")

        message = f"ChatBot: {username} se ha unido!".encode('utf-8')
        broadcast(message, client)
        client.send("Connected to server".encode('utf-8'))
        
        thread = threading.Thread(target = handle_messages, args = (client,))
        thread.start()

receive_connections()
