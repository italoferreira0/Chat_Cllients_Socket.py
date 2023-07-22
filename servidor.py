import threading
import socket

ListaCliente = []
MAXBYTES = 65535
ListaNomes = []


def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM )

    servidor.bind(('127.0.0.1',50000))
    servidor.listen()
   
    while True:
        cliente, addrees = servidor.accept()
        
        nomeUsuario = cliente.recv(MAXBYTES).decode()

        if nomeUsuario in ListaNomes:
            for nomeUsuario in ListaNomes:
                msg = "Invalido"
                cliente.send(msg.encode())
                nomeUsuario = cliente.recv(MAXBYTES).decode()
        
        cliente.send(nomeUsuario.encode())

        ListaCliente.append(cliente)
        ListaNomes.append(nomeUsuario)
        print(nomeUsuario, 'entrou no chat.')

        #print(ListaNomes)
        t1 = threading.Thread(target=receberMSG, args=[cliente,nomeUsuario]).start()
        
def receberMSG(cliente,nomeUsuario):
    while True:
        try:
            msg = cliente.recv(MAXBYTES)
            sairDoChat(msg,cliente,nomeUsuario)
            #print(msg.decode())
            enviarMSG(msg, cliente)

        except:
            ListaCliente.remove(cliente)
            ListaNomes.remove(nomeUsuario)
            print(nomeUsuario,' saiu do chat.')
        
            break
        
        #print(msg.decode())

def enviarMSG(msg, cliente): #Envia a mensagem para todos os clientes, exceto quem enviou.
    for clienteDiferente in ListaCliente:
        if clienteDiferente != cliente:
            clienteDiferente.send(msg)  

def sairDoChat(msg,cliente,nomeUsuario):
    if msg.decode() == 'SAIR':
        ListaCliente.remove(cliente)
        ListaNomes.remove(nomeUsuario)
        print(nomeUsuario,' saiu do chat.')
        cliente.close()


if __name__ == '__main__':
	main()
