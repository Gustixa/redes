import socket
import struct
import time

from crc32 import *
from hamming import *

NOISE_FACTOR = 0.0

def start_client(host='127.0.0.1', port=65432, message='Hello, World!'):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
		client_socket.connect((host, port))

		while True:
			data = encode_hamming(str_to_bits(message))
			crc = crc32_encode(data)
			#print(f"Message: {bits_to_str(decode_hamming(data))}")
			#print(f"Clean Data: {list_str(data)}")
			noisy_data = flip_bit_with_probability(data, NOISE_FACTOR)
			#print(f"Noisy Data: {list_str(noisy_data)}")
			client_socket.sendall(list_str(noisy_data).encode() + struct.pack('!I', crc))

			response = client_socket.recv(1024)
			if response:
				data = [int(bit) for bit in str(response[:-4])[2:-1]]
				crc_rec = struct.unpack('!I', response[-4:])[0]
				crc_calc = crc32_encode(data)
				is_valid_calc = crc32_verify(data, crc_calc)
				is_valid_rec = crc32_verify(data, crc_rec)
				#print(f"Received data encoded: {list_str(data)}")
				try:
					ham = decode_hamming(data)
					print(f"\033[32m[Hamming]\033[0m decoded: {list_str(ham)}")
				except: print("\033[31m[Hamming]\033[0m Failed to decode Hamming")
				try: print(f"\033[32m[Message]\033[0m data: {bits_to_str(ham)}")
				except: print("\033[31m[Message]\033[0m Failed to decode Message")
				#print(f"Received   CRC32: {crc_rec:#010x}")
				#print(f"Calculated CRC32: {crc_calc:#010x}")
				#print(f"Rec  CRC32 valid: {is_valid_rec}")
				#print(f"Calc CRC32 valid: {is_valid_calc}")
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