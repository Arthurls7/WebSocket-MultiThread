import socket   
import threading

host = '127.0.0.1'
port = 55555
FORMAT = "utf-8"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f"Server info: {host}:{port}")

clients = []
usernames = []
rooms = []

def sendMsg(message, _client):
    i = int(0)
    for client in clients:
        if client == _client:
            break
        i+=1

    j = int(0)
    for client in clients:
        if client != _client and rooms[i] == rooms[j]:
            client.send(message)
        j+=1

def recvMsg(client):
    while True:
        try:
            message = client.recv(1024)
            sendMsg(message, client)
        except:
            index = clients.index(client)
            username = usernames[index]
            sendMsg(f"Server: {username} disconnected!".encode(FORMAT), client)
            clients.remove(client)
            usernames.remove(username)
            rooms.pop(index)
            client.close()
            break

def recvConn():
    while True:
        client, address = server.accept()

        client.send("@username".encode(FORMAT))
        username = client.recv(1024).decode(FORMAT)
        clients.append(client)
        usernames.append(username)

        client.send("@room".encode(FORMAT))
        room = client.recv(1024).decode(FORMAT)
        rooms.append(int(room))
        
        print(f"{username} joined in Room: {room}, conn info: {str(address)}")

        message = f"Server: {username} joined the room!".encode(FORMAT)
        sendMsg(message, client)
        client.send("Connected to server".encode(FORMAT))

        thread = threading.Thread(target=recvMsg, args=(client,))
        thread.start()

def main():
    global server
    server.bind((host, port))
    server.listen()
    recvConn()

main()
