import socket
import threading

# Connection Data
host = socket.gethostbyname(socket.gethostname())
port = 55556

# Starting Server
# AF_INET = internet socket
# SOCK_STREAM = TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []
print("██████╗██╗  ██╗ █████╗ ████████╗████████╗███████╗██████╗") 
print("██╔════╝██║  ██║██╔══██╗╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗")
print("██║     ███████║███████║   ██║      ██║   █████╗  ██████╔╝")
print("██║     ██╔══██║██╔══██║   ██║      ██║   ██╔══╝  ██╔══██╗")
print("╚██████╗██║  ██║██║  ██║   ██║      ██║   ███████╗██║  ██║")
print(" ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝")
print(" /\   | _  _ _ |   _|_  _ _|_   _ _  _  _  _")
print("/~~\  |(_)(_(_||  (_| |(_| |   _\(/_|\/(/_|\n")
print("\nYour local network IP address is {}. \nFor someone to join server, they must use this IP address for client side script.".format(host))

# Sending Messages To All Connected Clients


def broadcast(message):
    for client in clients:
        client.send(message)

# Handling Messages From Clients


def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

# Receiving / Listening Function


def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()
