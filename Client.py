import socket   
import threading

username = input("Enter your username: ")
room = input("Enter the room number: ")

while room.isnumeric == False:
    room = input("Invalid room, try another: ")
    
host = '127.0.0.1'
port = 55555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

def recvMsg():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')

            if message == "@username":
                client.send(username.encode("utf-8"))
            elif message == "@room":
                client.send(room.encode("utf-8"))
            else:
                print(message)
        except:
            print("Error, closing connection")
            client.close()
            break

def sendMsg():
    while True:
        message = f"{username}: {input('')}"
        client.send(message.encode('utf-8'))

def main():
    threading.Thread(target=recvMsg).start()
    threading.Thread(target=sendMsg).start()

main()
