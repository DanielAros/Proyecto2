from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from random import randint

usuario = input("Escriba su nombre de usuario: ")
#iniciamos el cliente y mostramos su info
class Client(DatagramProtocol):    
    def __init__(self, host, port):
        if host == "localhost":
            host = "127.0.0.1"
#127.0.0.1
        self.id = usuario, host, port
        self.address = None
        self.server = '127.0.0.1', 9999
        print("ID actual:", self.id)

    def startProtocol(self):
#le mandamos nuestros datos al servidor
        self.transport.write(usuario.encode("utf-8"), self.server)

    def datagramReceived(self, datagram, addr):
#recibimos la información
        datagram = datagram.decode('utf-8')
#Nos conectamos con otro cliente        
        if addr == self.server:
            print("Seleccione un cliente\n", datagram)
            self.address = input("Escriba el host:"), int(input("Escriba el puerto:"))
#Creamos un hilo para mandar mensajes
            reactor.callInThread(self.send_message)
        else:
            #Se muestra el mensaje que fue recibido
            print(addr, ":", datagram)

#Mandamos el mensaje por el chat
    def send_message(self):
        while True:
            self.transport.write(input(":::").encode('utf-8'), self.address)


#puerto aleatorio para conectarse
if __name__ == '__main__':
    port = randint(1000, 5000)
    reactor.listenUDP(port, Client('localhost', port))
    reactor.run()
