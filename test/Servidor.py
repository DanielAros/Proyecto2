import socket
import threading

host = 'LocalHost'
port = 55555

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor.bind((host, port))
servidor.listen()
print("Sevidor esperando")

clientes = []
nombreUsuarios = []

def broadcast(message, _cliente):
    for cliente in clientes:
        if cliente != _cliente:
            cliente.send(message)

def manejar_mensajes(cliente):
    while True:
        try:
            mensaje = cliente.recv(1024)
            broadcast( mensaje, cliente)
        except:
            index = clientes.index(cliente)
            nombreUsuario = nombreUsuarios[index]
            broadcast(f"chat: {nombreUsuario} se ha desconectado".encode('utf-8'))
            clientes.remove(cliente)
            nombreUsuario.remove(nombreUsuario)
            cliente.close()
            break

def recibir_conexiones():
    while True:
        cliente, address = servidor.accept()
        cliente.send("@username".encode('utf-8'))
        nombreUsuario = cliente.recv(1024).decode('utf-8')

        clientes.append(cliente)
        nombreUsuarios.append(nombreUsuario)

        print(f"{nombreUsuario} esta conectado {str(address)}")

        message = f"Chat: {nombreUsuario} se ha unido!".encode('utf-8')
        broadcast(message, cliente)
        cliente.send("Conectado".encode('utf-8'))
        
        thread = threading.Thread(target = manejar_mensajes, args = (cliente,))
        thread.start()

recibir_conexiones()
