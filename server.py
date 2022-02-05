""" This is just the server and it just broadcast the messages. """

from contextlib import closing
import socket
import threading

HOST = '127.0.0.1' # ip (localhost)
PORT = 9090


# AF_INET ==> internet socket
# SOCK_STREAM ==> TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((HOST, PORT))

server.listen(2)

clients = []
nickNames = []


# Broadcast messages 
def broadcast(message):
  """
  Sends one message to all the clients
  Arguments: message
  """
  for client in clients:
    client.send(message)




# Handle
def handle(client):
  """ Handle Connections """
  while True:
    try:
      message = client.recv(1024) # 1024 Bytes 
      print(f'{nickNames[clients.index(client)]} says {message}')
      broadcast(message) # Broadcast to all users in server
    except:
      # if does not connected
      index = clients.index(client)
      clients.remove(client)
      client.close()

      nickname = nickNames[index]
      nickNames.remove(nickname)
      break




# Receive messages
def receive():
  """ Accept new client connections """

  while True:
    # Accept connection
    client,  address = server.accept()
    print(f'Connected with {str(address)}')

    # Give it a nickname
    client.send('NIC'.encode('utf-8'))
    nickname = client.recv(2048)

    # Add to database(Running DB)
    clients.append(client)
    nickNames.append(str(nickname))

    print(f'Nickname of joined client is {nickname}') # server-side message
    broadcast(f'{nickname} joined the chat 😀\n'.encode('utf-8'))
    client.send('Connected to the server.'.encode('utf-8')) # Just for this client send

    thread = threading.Thread(target=handle, args=(client,))
    thread.start()


print('Server is running... Have fun 😉')
receive()


