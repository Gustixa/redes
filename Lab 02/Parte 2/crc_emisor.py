import socket
import struct
import time

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

def start_client(host='127.0.0.1', port=65432, message='Hello, World!'):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
		client_socket.connect((host, port))

		while True:
			client_socket.sendall(message.encode())

			response = client_socket.recv(1024)
			if response:
				data = response[:-4]
				crc_received = struct.unpack('!I', response[-4:])[0]
				is_valid = crc32_verify(data, crc_received)
				print(f"Received data: {data.decode()}")
				print(f"Received CRC32: {crc_received:#010x}")
				print(f"CRC32 is valid: {is_valid}")
				time.sleep(2.5)

if __name__ == '__main__':
	start_client()