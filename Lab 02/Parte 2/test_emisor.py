import socket
import struct
import time

from crc32 import *
from hamming import *

NOISE_FACTOR = 0.5

def start_client(host='127.0.0.1', port=65432, message='Hello, World!'):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
		client_socket.connect((host, port))

		while True:
			data = encode_hamming(str_to_bits(message))
			crc = crc32_encode(data)
			noisy_data = bit_noise(data, NOISE_FACTOR)
			client_socket.sendall(list_str(noisy_data).encode() + struct.pack('!I', crc))

			response = client_socket.recv(1024)
			if response:
				data = [int(bit) for bit in str(response[:-4])[2:-1]]
				crc_rec = struct.unpack('!I', response[-4:])[0]
				crc_calc = crc32_encode(data)
				is_valid_calc = crc32_verify(data, crc_calc)
				is_valid_rec = crc32_verify(data, crc_rec)
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
				time.sleep(2.5)

if __name__ == '__main__':
	start_client()