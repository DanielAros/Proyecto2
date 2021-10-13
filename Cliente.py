from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from random import randint

class Client(DatagramProtocol):
    def __init__(self, host, port):
        if host == "localhost":
            host = "192.168.1.252"

        self.id = host, port
        self.address = None
        self.server = '192.168.1.252', 9999
        print("ID actual:", self.id)

    def startProtocol(self):
        self.transport.write("ready".encode("utf-8"), self.server)

    def datagramReceived(self, datagram, addr):
        datagram = datagram.decode('utf-8')

        if addr == self.server:
            print("Seleccione un cliente\n", datagram)
            self.address = input("Escriba el host:"), int(input("Escriba el puerto:"))
            reactor.callInThread(self.send_message)
        else:
            print(addr, ":", datagram)

    def send_message(self):
        while True:
            self.transport.write(input(":::").encode('utf-8'), self.address)

if __name__ == '__main__':
    port = randint(1000, 5000)
    reactor.listenUDP(port, Client('localhost', port))
    reactor.run()
