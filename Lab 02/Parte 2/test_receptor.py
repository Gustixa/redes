import socket
import struct

from crc32 import *
from hamming import *

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
				print(f"Received data encoded: {data.decode()}")
				print(f"Received data decoded: {decode_hamming(data.decode())}")
				print(f"Received data : {bit_list_to_string(decode_hamming(data.decode()))}")
				print(f"Received CRC32: {crc:#010x}")
				print(f"CRC32 is valid: {is_valid}")
				conn.sendall(data + struct.pack('!I', crc))

if __name__ == '__main__':
	start_server()