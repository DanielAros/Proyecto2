import socket
import sys
import threading
from random import randint

servidor = ('127.0.0.1', 55555)

# connect to servidor
print('Conectando con el servidor')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

puerto = randint(1000, 5000)


direccion = '127.0.0.'
direccion += str(randint(2,10))

print(direccion)
print(type(direccion))

sock.bind((direccion, puerto))

sock.sendto(b'0', servidor)

while True:
    data = sock.recv(1024).decode()

    if data.strip() == 'ready':
        print('Registrando con el servidor, esperando')
        break

data = sock.recv(1024).decode()
ip, sport, dport = data.split(' ') #S recibe la informacion del otro cliente
sport = int(sport) #Recibimos el puerto del otro cliente
dport = int(dport)

print("Sport")
print(sport)
print("dport")
print(dport)

#myHostName = socket.gethostname()

#myIp = socket.gethostbyname(myHostName)
#print("Mi ip {}".format(myIp))

print('\ngot peer')
print('  ip:          {}'.format(ip))
print('  source port: {}'.format(sport))
print('  dest port:   {}\n'.format(dport))

# punch hole
# equiv: echo 'punch hole' | nc -u -p 50001 x.x.x.x 50002
print('Conectando')

#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.bind((direccion, puerto))
sock.sendto(b'0', (ip, sport))

print('Listo para intercambiar mensajes\n')

# listen for
# equiv: nc -u -l 50001
def listen():
    #sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #sock.bind((direccion, sport))

    while True:
        data = sock.recv(1024)
        print('\rpeer: {}\n> '.format(data.decode()), end='')

listener = threading.Thread(target=listen, daemon=True);
listener.start()

# send messages
# equiv: echo 'xxx' | nc -u -p 50002 x.x.x.x 50001
#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.bind((ip, sport))

while True:
    msg = input('> ')
    sock.sendto(msg.encode(), (ip, sport))