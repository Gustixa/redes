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
				response = conn.recv(1024)
				if response:
					data = [int(bit) for bit in str(response[:-4])[2:-1]]
					crc_rec = struct.unpack('!I', response[-4:])[0]
					crc_calc = crc32_encode(data)
					is_valid_calc = crc32_verify(data, crc_calc)
					is_valid_rec = crc32_verify(data, crc_rec)
					print(f"Received data encoded: {list_str(data)}")
					print(f"Received data decoded: {list_str(decode_hamming(data))}")
					print(f"Received message: {bits_to_str(decode_hamming(data))}")
					print(f"Received   CRC32: {crc_rec:#010x}")
					print(f"Calculated CRC32: {crc_calc:#010x}")
					print(f"Rec  CRC32 valid: {is_valid_rec}")
					print(f"Calc CRC32 valid: {is_valid_calc}")
					conn.sendall(list_str(data).encode() + struct.pack('!I', crc_calc))
				else: break

if __name__ == '__main__':
	start_server()