import socket
import struct
import time

from crc32 import *
from hamming import *

def start_client(host='127.0.0.1', port=65432, message='Hello, World!'):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
		client_socket.connect((host, port))

		while True:
			client_socket.sendall(encode_hamming(string_to_bit_list(message)).encode())

			response = client_socket.recv(1024)
			if response:
				data = response[:-4]
				crc_received = struct.unpack('!I', response[-4:])[0]
				is_valid = crc32_verify(data, crc_received)
				print(f"Received data encoded: {data.decode()}")
				print(f"Received data decoded: {decode_hamming(data.decode())}")
				print(f"Received data : {bit_list_to_string(decode_hamming(data.decode()))}")
				print(f"Received CRC32: {crc_received:#010x}")
				print(f"CRC32 is valid: {is_valid}")
				time.sleep(2.5)

if __name__ == '__main__':
	start_client()