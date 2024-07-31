import socket
import struct

def generate_crc32_table():
	polynomial = 0xEDB88320
	table = []
	for i in range(256):
		crc = i
		for j in range(8):
			if (crc & 1) != 0:
				crc = (crc >> 1) ^ polynomial
			else:
				crc >>= 1
		table.append(crc)
	return table

def crc32_encode(data):
	crc32_table = generate_crc32_table()
	crc = 0xFFFFFFFF
	for byte in data:
		crc = crc32_table[(crc ^ byte) & 0xFF] ^ (crc >> 8)
	return crc ^ 0xFFFFFFFF

def crc32_verify(data, provided_checksum):
	computed_checksum = crc32_encode(data)
	return computed_checksum == provided_checksum

def start_server(host='127.0.0.1', port=65432):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
		server_socket.bind((host, port))
		server_socket.listen()
		print(f"Server listening on {host}:{port}")

		conn, addr = server_socket.accept()
		print(f"Connected by {addr}")
		with conn:
			while True:
				data = conn.recv(1024)
				if not data:
					break
				crc = crc32_encode(data)
				is_valid = crc32_verify(data, crc)
				print(f"Received data: {data.decode()}")
				print(f"Received CRC32: {crc:#010x}")
				print(f"CRC32 is valid: {is_valid}")
				conn.sendall(data + struct.pack('!I', crc))

if __name__ == '__main__':
	start_server()