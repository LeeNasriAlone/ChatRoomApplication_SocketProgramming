import socket
import select

HEADER_LENGTH = 1024
IP = "localhost"
PORT = 22875
FORMAT = 'utf-8'

# create socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Assign basic information to the socket object.
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind( (IP, PORT) )
# Wait for the connection from the client.
server.listen()
# list of all sockets. now, we have server( server_socket ). 
sockets_list = [server]
# client dictionary where clients socket will be the key and
# user data can be the value.
clients = {}
print(f'Wait for connections on IP : {IP} , PORT : {PORT}...')
 
def receive_message(client):
	try:
		header = client.recv(HEADER_LENGTH)
		# if there is no any message.
		if not len(header):
			return False

		# else
		length = int(header.decode(FORMAT).strip())
		return {
			'header': header,
			'data': client.recv(length)
		}

	except:
		return False

while True:
	sockets, x, exceptionOfSockets = select.select(sockets_list, [], sockets_list)

	for socket in sockets:
		# if someone just connected then accepte the connection.
		if socket == server:
			clientSocket, clientAddress = server.accept()
			# receive message from that client.
			user_new_message = receive_message( clientSocket )
			# if user is disconnected => leave the loop
			if user_new_message is False:
				continue

			# else => add client socket to the sockets_list and clients dictionary.
			sockets_list.append(clientSocket)
			clients[clientSocket] = user_new_message
			print('New connection from {}:{}, username: {}'.format(*clientAddress, user_new_message['data'].decode(FORMAT)))
			#print(f"Accepted new connection from {clientAddress[0]}:{clientAddress[1]} username:{user['data'].decode['utf-8']}")

		# if there is no new connection then server receive message again.
		else:
			user_old_message = receive_message(socket)

			# if there is no message from that client => closed the connection and delete from client dictionary.
			if user_old_message is False:
				print(f"Closed connection from {clients[socket]['data'].decode(FORMAT)}")
				sockets_list.remove(socket)
				del clients[socket]
				continue

			# if there is a message.
			user = clients[socket]
			print(f'Received message from {user["data"].decode(FORMAT)}: {user_old_message["data"].decode(FORMAT)}')

			# show the message to other clients.
			for clientSocket in clients:
				if clientSocket != socket:
					clientSocket.send(user['header'] + user['data'] + user_old_message['header'] + user_old_message['data'])


	for socket in exceptionOfSockets:
		sockets_list.remove(socket)
		del clients[socket]
