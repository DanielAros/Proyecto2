from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from random import randint

#iniciamos el cliente y mostramos su info
class Client(DatagramProtocol):
    def __init__(self, host, port):
        if host == "localhost":
            host = "192.168.1.252"
#127.0.0.1
        self.id = host, port
        self.address = None
        self.server = '192.168.1.252', 9999
        print("ID actual:", self.id)

    def startProtocol(self):
#le mandamos nuestros datos al servidor
        self.transport.write("ready".encode("utf-8"), self.server)

    def datagramReceived(self, datagram, addr):
#recibimos los clientes que ya estan conectados
        datagram = datagram.decode('utf-8')
#Nos conectamos con otro cliente        
        if addr == self.server:
            print("Seleccione un cliente\n", datagram)
            self.address = input("Escriba el host:"), int(input("Escriba el puerto:"))
#Creamos un hilo para mandar mensajes
            reactor.callInThread(self.send_message)
        else:
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
