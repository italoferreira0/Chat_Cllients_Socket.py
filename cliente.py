import threading
import socket

MAXBYTES = 65535

def main():

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    cliente.connect(('127.0.0.1', 50000))

    nomeUsuario = input('Digite seu nome: ')
    cliente.send(nomeUsuario.encode())
    msg = cliente.recv(MAXBYTES).decode()

    while msg == "Invalido":
        print('Esse nome já está sendo usado, tente outro')
        nomeUsuario = input('Digite seu nome: ')
        cliente.send(nomeUsuario.encode())
        msg = cliente.recv(MAXBYTES).decode()

    print(nomeUsuario,' está conectado.')
    
    
    t1 = threading.Thread(target=ReceberMSG, args=[cliente]).start()               #As duas Threads vão
    t2 = threading.Thread(target=EnviarMSG, args=[cliente, nomeUsuario]).start()   #rodar ao mesmo tempo.
    
    #EnviarMSG(cliente, nomeUsuario)
    #ReceberMSG(cliente)

def ReceberMSG(cliente):
    while True: #Enqunto estiver conectado o servidor vai está sempre enviando algo para o cliente.
        msg = cliente.recv(MAXBYTES).decode()
        print(msg)

def EnviarMSG(cliente, nomeUsuario):
    while True: 
        msg = input('')
        cliente.send('{}: {}'.format(nomeUsuario, msg).encode())
        sairDoChat(msg,cliente)

def sairDoChat(msg,cliente):
    try:
        while msg == 'SAIR':
            cliente.close()
            break
    except:
        while True:
            cliente.close()
            break
        
if __name__ == '__main__':
	main()

