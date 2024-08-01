import socket
import struct

from crc32 import *
from hamming import *

def start_server(host='127.0.0.1', port=8888):
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
					is_valid_rec = crc32_verify(data, crc_rec)
					crc_calc = crc32_encode(data)
					is_valid_calc = crc32_verify(data, crc_calc)
					try:
						ham = decode_hamming(data)
						print(f"\033[32m[Hamming]\033[0m decoded: {list_str(ham)}")
					except Exception as e: print(f"\033[31m[Hamming]\033[0m Failed to decode Hamming [{e}]")
					try: print(f"\033[32m[Message]\033[0m data: {bits_to_str(ham)}")
					except Exception as e: print(f"\033[31m[Message]\033[0m Failed to decode Message [{e}]")
					if is_valid_rec and is_valid_calc and crc_rec == crc_calc:
						print(f"\033[32m[CRC32]\033[0m Verified")
					else:
						print(f"\033[31m[CRC32]\033[0m Failed")
						print(f"\033[31m[CRC32]\033[0m Received  : {crc_rec:#10x}")
						print(f"\033[31m[CRC32]\033[0m Calculated: {crc_calc:#10x}")
					print("|---------------------------------")
					conn.sendall(list_str(data).encode() + struct.pack('!I', crc_calc))
				else: break

if __name__ == '__main__':
	start_server()