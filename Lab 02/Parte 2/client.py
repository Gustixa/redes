import socket

def encode_message(message):
	binary_message = ''.join(format(ord(char), '08b') for char in message)
	checksum = calculate_checksum(binary_message)
	return binary_message + checksum

def calculate_checksum(binary_message):
	total = sum(int(binary_message[i:i+8], 2) for i in range(0, len(binary_message), 8))
	checksum = format((256 - total % 256) % 256, '08b')
	return checksum

def main():
	# Crear socket
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	# Conectar al servidor
	client_socket.connect(("localhost", 8080))
	
	# Enviar mensaje
	message = "Hola, servidor!"
	binary_message = encode_message(message)
	client_socket.sendall(binary_message.encode())
	
	# Cerrar socket
	client_socket.close()

if __name__ == "__main__":
	main()