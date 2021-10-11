import socket
import threading

nombreUsuario = input("Ingresa un nombre de usuario: ")

host = 'LocalHost'
port = 55555

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((host, port))

def recibir_mensaje():
    while True:
        try:
            mensaje = cliente.recv(1024).decode('utf-8')
            if mensaje == "@username":
                cliente.send(nombreUsuario.encode("utf-8"))
            else:
                print(mensaje)
        except:
            print("Error")
            cliente.close
            break

def escribir_mensaje():
    while True:
        mensaje = f"{nombreUsuario}: {input('')}"
        cliente.send(mensaje.encode('utf-8'))

recibir_hilo = threading.Thread(target = recibir_mensaje)
recibir_hilo.start()

escribir_mensaje = threading.Thread(target = escribir_mensaje)
escribir_mensaje.start()
