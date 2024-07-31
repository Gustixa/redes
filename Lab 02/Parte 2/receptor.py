import socket

def main():
	host = '127.0.0.1'
	port = 8888

	# Crear socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))

	# Escuchar conexiones entrantes
	s.listen(1)
	print("Esperando conexión...")

	conn, addr = s.accept()
	print(f"Conectado por {addr}")

	while True:
		data = conn.recv(1024)
		if not data:
			break
		print(f"Mensaje recibido: {data.decode()}")

	conn.close()

if __name__ == "__main__":
	main()