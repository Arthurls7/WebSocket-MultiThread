import socket 
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 8081
ADDR = (IP, PORT)
FORMAT = "utf-8"

def imprimir(tupla):
    for i in tupla:
        print(i)

def jogo_cliente(conn, addr):
    palavra = "teste"
    hifens = ['_', '_', '_', '_', '_']
    tupla = ['t', 'e', 's', 't', 'e'] 
    acertos = 0
    chances = 5

    #dando boas vindas
    boas_vindas = "Bem vindo ao jogo da forca, insira seu nome: "
    conn.send(boas_vindas.encode(FORMAT))

    #recebendo o nome e iniciando o jogo
    name = conn.recv(1024).decode(FORMAT)
    msg = f"\nBom jogo {name}"
    conn.send(msg.encode(FORMAT))

    
    while True:
        if acertos == len(palavra):
            msg = f"Parabens {name}, voce conseguiu!\n"
            conn.send(msg.encode(FORMAT))
            conn.close()
            return
        elif chances == 0:
            msg = "Infelizmente nao foi dessa vez :( \n"
            conn.send(msg.encode(FORMAT))
            conn.close()
            return
            
        
        msg = f"\nPalavra: {hifens}\nSua entrada: "
        conn.send(msg.encode(FORMAT))
        #msg = "Tentativas restantes:"
        #conn.send(msg.encode(FORMAT))
        
        msg = conn.recv(56).decode(FORMAT)
        print(f"Msg recebida: {msg}")
        
        salvaAcerto = acertos
        for i in range(len(palavra)):
            print(f"Tupla: {tupla[i]} - Msg: {msg}\n")
            print("Nova jogada:\n")
            if tupla[i] == msg:
                acertos += 1
                hifens[i] = tupla[i]
                print("Entrou no acerto\n")
            else:
                print("Entrou no erro")
                
        if salvaAcerto == acertos:
            chances -= 1            
            
def main(): 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    timeoutCounter = 0
    
    while True:
        try:
            print(f"[Conexoes ativas: {threading.activeCount()-1}]")
            conn, addr = server.accept()
            #Agora ja temos o socket criado e aceitando conexoes
            #A partir daqui sera implementado a multi-thread

            thread = threading.Thread(target=jogo_cliente, args=(conn,addr))
            thread.start()
        except:
            print(f"Timeout no servidor, conexoes nao ativas")
        #    timeoutCounter += 1
        #finally:
        #    if timeoutCounter > 2:
        #        print(f"Finalizando devido a multiplos timeouts...")
        #        exit()

#iniciando o programa
socket.setdefaulttimeout(120)
main()
