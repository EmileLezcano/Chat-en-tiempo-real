import socket
import threading

# Datos de conexión
host = '127.0.0.1'
port = 9999

# Iniciando el servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Listas de clientes y sus apodos
clients = []
nicknames = []

# Envío de mensajes a todas las clientas conectadas
def broadcast(message):
    for client in clients:
        client.send(message)

# Manejo de mensajes de clientes
def handle(client):
    while True:
        try:
            # Mensajes de difusión
            message = client.recv(1024)
            broadcast(message)
        except:
            # Eliminar cliente desconectado
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} ha salido del chat'.encode('ascii'))
            nicknames.remove(nickname)
            break

# Función de recepción/escucha
def receive():
    print(f"Servidor iniciado en {host}:{port}")
    while True:
        try:
            # Aceptar conexión
            client, address = server.accept()
            print(f"Conectado a {str(address)}")

            # Solicitar y almacenar apodo
            client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            nicknames.append(nickname)
            clients.append(client)

            # Apodo para imprimir y transmitir
            print(f'{nickname} se ha conectado.')
            broadcast(f'{nickname} ha conectado al chat'.encode('ascii'))
            client.send('Conectado al chat'.encode('ascii'))

            # Comenzar a manejar el hilo para el cliente
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        except Exception as e:
            print(f"Error al aceptar conexión: {e}")

if __name__ == "__main__":
    receive()