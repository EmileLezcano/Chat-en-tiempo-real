import socket
import threading
import sys

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("Conexión cerrada.")
            client.close()
            break

def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('utf-8'))

# Crear un socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Intentar conectar al servidor
    client.connect(('127.0.0.1', 9999))
    print("Conectado al servidor exitosamente.")
except ConnectionRefusedError:
    print("No se pudo conectar al servidor. Asegúrate de que el servidor esté en ejecución.")
    sys.exit()
except Exception as e:
    print(f"Ocurrió un error al intentar conectar: {e}")
    sys.exit()

# Elegir un apodo después de conectarse exitosamente
nickname = input("Ingrese su Nombre: ")

# Iniciar hilos para escuchar y escribir
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()