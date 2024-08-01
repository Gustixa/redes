import socket
import struct
import time

from crc32 import *
from hamming import *

NOISE_FACTOR = 0.0
MULTI_ERROR_FACTOR = 0.01

def select_random_words(filename, num_words):
	return ' '.join(random.sample(open(filename, 'r').read().split(), num_words))

def start_client():
	host='127.0.0.1'
	port=8888
	open('Log.txt', 'w').write("|------------------------------------------------------------------------------------")
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
		client_socket.connect((host, port))
		while True:
			message = select_random_words("Words.txt", random.randrange(3,8))
			data = encode_hamming(str_to_bits(message))
			crc = crc32_encode(str_to_bits(message))
			noisy_data = hamming_noise(data, NOISE_FACTOR, MULTI_ERROR_FACTOR)

			open('Log.txt', 'a').write(f"\n[Send] message: {message}")
			open('Log.txt', 'a').write(f"\n[Send] hamming: {list_str(data)}")
			open('Log.txt', 'a').write(f"\n[Send] noisy  : {list_str(noisy_data)}")

			client_socket.sendall(list_str(noisy_data).encode() + struct.pack('!I', crc))

			response = client_socket.recv(1024)
			if response:
				data = [int(bit) for bit in str(response[:-4])[2:-1]]
				crc_rec = struct.unpack('!I', response[-4:])[0]
				ham, err = decode_hamming(data)
				crc_calc = crc32_encode(ham)
				if crc_rec != crc_calc:
					print(f"\033[31m[CRC32]\033[0m Failed {crc_rec:#10x} != {crc_calc:#10x}")
					open('Log.txt', 'a').write(f"\n[CRC32] Failed {crc_rec:#10x} != {crc_calc:#10x}")
				else:
					print(f"\033[32m[CRC32]\033[0m Verified {crc_rec:#10x} == {crc_calc:#10x}")
					open('Log.txt', 'a').write(f"\n[CRC32] Verified {crc_rec:#10x} == {crc_calc:#10x}")

					open('Log.txt', 'a').write(f"\n[Hamming] errors: {err}")
					print(f"\033[32m[Hamming]\033[0m decoded: {list_str(ham)}")
					open('Log.txt', 'a').write(f"\n[Hamming] decoded: {list_str(ham)}")
					print(f"\033[32m[Rec]\033[0m : {bits_to_str(ham)}")
					open('Log.txt', 'a').write(f"\n[Rec] : {bits_to_str(ham)}")
				print("|------------------------------------------------------------------------------------")
				open('Log.txt', 'a').write("\n|------------------------------------------------------------------------------------")
				time.sleep(2.5)

if __name__ == '__main__':
	start_client()