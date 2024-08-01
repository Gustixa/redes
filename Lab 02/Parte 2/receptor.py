import socket
import struct

from crc32 import *
from hamming import *

def start_server():
	host='127.0.0.1'
	port=8888

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
		server_socket.bind((host, port))
		server_socket.listen()
		print(f"Server listening on {host}:{port}")

		conn, addr = server_socket.accept()
		with conn:
			while True:
				response = conn.recv(1024)
				if response:
					data = [int(bit) for bit in str(response[:-4])[2:-1]]
					crc_rec = struct.unpack('!I', response[-4:])[0]
					ham, err = decode_hamming(data)
					crc_calc = crc32_encode(ham)
					if crc_rec != crc_calc:
						print(f"\033[31m[CRC32]\033[0m Failed {crc_rec:#10x} != {crc_calc:#10x}")
					else:
						print(f"\033[32m[CRC32]\033[0m Verified {crc_rec:#10x} == {crc_calc:#10x}")
						print(f"\033[32m[Hamming]\033[0m decoded: {list_str(ham)}")
						print(f"\033[32m[Rec]\033[0m : {bits_to_str(ham)}")
					print("|------------------------------------------------------------------------------------")
					conn.sendall(list_str(data).encode() + struct.pack('!I', crc_rec))
				else: break

if __name__ == '__main__':
	start_server()