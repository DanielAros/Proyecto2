import socket
import threading
from random import randint

servidor = ('localhost', 55555)

# connect to servidor
print('')
print('=========== Conectando con el servidor ===========')
print('')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

direccion = '127.0.0.1' #Esta dirección es quivalente a poner localhost
puerto = randint(1000, 5000)

print('******** Tu dirección: "{}", '.format(direccion) + 'tu puerto: "{}" ********'.format(puerto))

sock.bind((direccion, puerto))

print('=========== Registrando con el servidor... ===========')

sock.sendto(b'0', servidor)

while True:
    data = sock.recv(128).decode()

    if data.strip() == 'Hecho':
        print('')
        print('========= Registro correcto, esperando datos del otro Cliente... =========')
        print('')
        break

data = sock.recv(1024).decode()
dip, dport, = data.split(' ') #S recibe la informacion del otro cliente
dport = int(dport) #Recibimos el puerto del otro cliente

print('Datos recibidos con éxito!')
print('')
print('Dirección de Destino: "{}"'.format(dip))
print('Puerto de Destino: "{}"'.format(dport))
print('')

print('=========== Conectando... ===========')
print('')

sock.sendto(b'0', (dip, dport)) #Enviamos un 0 para establecer la conexión

data = sock.recv(128)   #Recibimos el 0 del otro equipo para establecer la conexión

print('=========== Listo para intercambiar mensajes ===========')
print('')
print('Tip: Escribe "exit" para salir. Sin comillas')
print('')

detener_hilos = False   #boleano para matar los hilos inicializado en falso

def escuchar():
    while True:
        data = sock.recv(2048).decode()  #Recibimos el mensaje

        global detener_hilos    #Leemos la variable global del boleano para matar los hilos

        if(data == 'exit'):    #Si el mensaje recibido dice "exit"...
            print('')
            print('')
            print('== El otro Cliente ha cerrado la conexión. Presiona "Enter" para salir ==')
            detener_hilos = True    #Cambiamos el valor a True para matar los hilos

        if(detener_hilos):  #Si el valor es True...
            break   #Matamos este hilo
        
        if '.jpg' in data:
            file = open('./images/imagenNueva.jpg', 'wb')
            image_part = sock.recv(2048)
            print("\nRecibiendo imagen")
            while image_part:
                file.write(image_part)
                image_part = sock.recv(2048)
            file.close()
            print("Recibido completo\nTú: > ")
        else: 
            print('\rCliente: {}\nTú: > '.format(data), end='')    #Si no dice exit, ni el bool es True, entonces mostramos el mensaje
       
def decir():
    while True:
        msg = input('Tú: > ')   #Leemos la consola
        
        sock.sendto(msg.encode(), (dip, dport)) #Mandamos el mensaje al otro cliente
        
        if '.jpg' in msg:
            file = open('./images/imgOriginal.jpg', 'rb')
            image_data = file.read(2048)
            while image_data:
                sock.sendto(image_data, (dip, dport))
                image_data = file.read(2048)
            sock.sendto(''.encode(), (dip, dport))#Envia un mensaje vacio para salir del ciclo de recibido
            file.close()

        global detener_hilos    #Leemos la variable global del boleano para matar los hilos

        if(msg == 'exit'):  #Si el mensaje que acabamos de mandar decía "exit..."
            print('')
            print('=========== Saliendo... ===========')
            detener_hilos = True    #Cambiamos el valor a True para matar los hilos

        if(detener_hilos):  #Si el valor es True...
            break   ##Matamos este hilo

escuchar = threading.Thread(target=escuchar, daemon=True)   #creamos el hilo para la función escuchar
decir = threading.Thread(target=decir)  #creamos el hilo para la función decir

escuchar.start()    #Iniciamos el hilo escuchar
decir.start()   #Iniciamos el hilo decir