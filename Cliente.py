import socket
import threading
from random import randint

servidor = ('localhost', 55555)

print('')
miUsuario = input('Escribe tu usuario: > ')

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

sock.sendto(miUsuario.encode(), servidor)

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

sock.sendto(miUsuario.encode(), (dip, dport)) #Enviamos el usuario para establecer la conexión

suUsuario = sock.recv(128).decode()   #Recibimos el usuario del otro equipo para establecer la conexión

print('=========== Listo para intercambiar mensajes ===========')
print('')
print('Tip: Escribe "exit" para salir. Sin comillas')
print('Tip: Escribe "NombreArchivo.extensión/envArch" para enviar un archivo. Sin comillas')
print('ASEGURATE DE QUE ANTES SE ENCUENTRE EN LA CARPETA DE "ARCHIVOS"')
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
        
        if '/envArch' in data:

            nombreArchivo = data.split('/') #Leemos el mensaje y lo partimos en donde está la "/" para separar el nombre y extensión del comando en sí

            file = open('./archivosR/' + nombreArchivo[0], 'wb')    #la posicion 0 de nombreArchivo contiene el nombre y extensión
            file_part = sock.recv(1024)
            print("\nRecibiendo archivo")
            while file_part:
                file.write(file_part)
                file_part = sock.recv(1024)
            file.close()
            print("Archivo Recibido")
            print(miUsuario + ': > ')
        else: 
            print('\r' + suUsuario + ': {}\n'.format(data) + miUsuario + ': > ', end='')    #Si no dice exit, ni el bool es True, entonces mostramos el mensaje
       
def decir():
    while True:
        msg = input(miUsuario + ': > ')   #Leemos la consola
        
        sock.sendto(msg.encode(), (dip, dport)) #Mandamos el mensaje al otro cliente
        
        if '/envArch' in msg:

            nombreArchivo = msg.split('/')  #Leemos el mensaje y lo partimos en donde está la "/" para separar el nombre y extensión del comando en sí

            file = open('./archivos/' + nombreArchivo[0], 'rb') #la posicion 0 de nombreArchivo contiene el nombre y extensión
            file_data = file.read(1024)
            while file_data:                           #Se podría implementar mejor con un Do-While y así se evita enviar el mensaje vacío
                sock.sendto(file_data, (dip, dport))
                file_data = file.read(1024)
            sock.sendto(''.encode(), (dip, dport))  #Envia un mensaje vacío para salir del ciclo de recibir
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