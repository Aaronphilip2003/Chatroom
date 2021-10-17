import threading
import socket

host='127.0.0.1' #localhost
port=55555

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# A pair (host, port) is used for the AF_INET address family, where host is a string representing either a hostname in internet domain notation like 'daring.cwi.nl' or an IPv4 address like '100.50.200.5', and port is an integer.

# SOCK_STREAM is the socket type for TCP, the protocol that will be used to transport our messages in the network.

server.bind((host,port))
#  bind() method which binds it to a specific IP and port so that it can listen to incoming requests on that IP and port.
server.listen()
# server.listen() Enable a server to accept connections. If backlog is specified, it must be at least 0 (if it is lower, it is set to 0); it specifies the number of unaccepted connections that the system will allow before refusing new connections. If not specified, a default reasonable value is chosen.

clients=[]
nicknames=[]

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message=client.recv(1024)
            broadcast(message)
        except:
            index=clients.index(client)
            clients.remove(client)
            client.close()
            nickname=nicknames[index]
            broadcast(f'{nickname} has left the chatroom!'.encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}')")

        client.send('NICK'.encode('ascii'))
        nickname=client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('Connected with the server!'.encode('ascii'))

        thread=threading.Thread(target=handle,args=(client,))
        thread.start()

print("Server is listening.....")
receive()
