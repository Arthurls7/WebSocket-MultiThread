import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 8081
ADDR = (IP, PORT)
FORMAT = "utf-8"

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    #recebe boas vindas
    msg = client.recv(1024).decode(FORMAT)
    print(msg)
    msg = input()

    #enviando o nome
    client.send(msg.encode(FORMAT))
    msg = client.recv(1024).decode(FORMAT)
    print(msg)

    msg = client.recv(1024).decode(FORMAT)
    print(msg)
    
    while True:
        msg = input()
        if len(msg) > 1:
            print("Insira apenas uma letra")
        else:
            client.send(msg.encode(FORMAT))
            msg = client.recv(1024).decode(FORMAT)
            print(msg)

main()
