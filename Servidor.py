from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

#iniciamos el servidor
class Server(DatagramProtocol):
    print("Servidor listo\n")
    def __init__(self):
        self.clients = set()

    def datagramReceived(self, datagram, addr):
        #Recibimos la direccion y el puerto del cliente
        datagram = datagram.decode("utf-8")
        #Añadimos al cliente
        print(datagram)
        addresses = "\n".join([str(x) for x in self.clients])
        print(addresses)
        self.transport.write(addresses.encode('utf-8'), addr)#Se envian los clientes disponibles
        self.clients.add(datagram + ": " + str(addr))

#Leer los puertos
if __name__ == '__main__':
    reactor.listenUDP(9999, Server())
    reactor.run()
