# 1. client tell the server what their username is
# 2. infinite loop of if clients have a message and also receive message.

import socket
import select
import errno
import sys
import threading
HEADER_LENGTH = 1024
IP = "localhost"
PORT = 22875
FORMAT = 'utf-8'

# create socket object.
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM )

# connect to the server.
client.connect( (IP, PORT) )
client.setblocking(False)

# enter username
usernameInput = input("Please enter username : ")
username = usernameInput.encode(FORMAT)
user_header = f"{len(username):<{HEADER_LENGTH}}".encode(FORMAT)

# send username to server
client.send(user_header + username)

def send_message():
	while True:
		user_message = input( )
		# if there is a message. => send to server
		if user_message:
			user_message = user_message.encode(FORMAT)
			user_message_header = f"{len(user_message) :< {HEADER_LENGTH}}".encode(FORMAT)
			client.send(user_message_header + user_message)

def receive_message():
	while True:
		try:
			# infinite loop for receive message from the server
			while True:
				# receive header
				server_username_header = client.recv(HEADER_LENGTH)

				# if we dot get any data
				if not len(server_username_header):
					print("connection closed by the server")
					sys.exit()

				server_username_length = int(server_username_header.decode(FORMAT).strip())
				server_username = client.recv(server_username_length).decode(FORMAT)


				# receive message
				server_message_header = client.recv(HEADER_LENGTH)
				server_message_length = int(server_message_header.decode(FORMAT).strip())
				server_message = client.recv(server_message_length).decode(FORMAT)
				print(f"{server_username} > {server_message}")

		except IOError as e:
			if e.errno != errno.EAGAIN or e.errno != errno.EWOULDBLOCK:
				print('Error : ', str(e))
				sys.exit()

			continue

		except Exception as e:
			print('General error', str(e))
			sys.exit()

# Create thread, first for send message and second for receive message.
threading.Thread(target=send_message).start()
threading.Thread(target=receive_message).start()



	
