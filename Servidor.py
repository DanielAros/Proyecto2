import socket

print('')
print('=========== Iniciando Servidor... ===========')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('localhost', 55555))

clients = []

print('=========== Servidor en espera ===========')
print('')

while True:
    data, address = sock.recvfrom(128)

    print('Se ha conectado: "{}"'.format(data.decode()) + ' desde: {}.'.format(address))
    clients.append(address)

    sock.sendto(b'Hecho', address)

    if len(clients) == 2:
        print('')
        print('Obtenidos 2 clientes, enviando detalles a cada uno...')
        print('')
        break

c1 = clients.pop()
c1_addr, c1_port = c1
c2 = clients.pop()
c2_addr, c2_port = c2

sock.sendto('{} {}'.format(c1_addr, c1_port).encode(), c2)
sock.sendto('{} {}'.format(c2_addr, c2_port).encode(), c1)

print('Datos Enviados con éxito!')
print('')
print('=========== Apagando Servidor... ===========')
print('')