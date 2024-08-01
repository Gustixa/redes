import socket
import struct

from crc32 import *
from hamming import *

NOISE_FACTOR = 0.1
MULTI_ERROR_FACTOR = 0.005
COUNT = 8192
PRINT = False
LOG = True

def select_random_words(filename, num_words):
	return ' '.join(random.sample(open(filename, 'r').read().split(), num_words))

def main():
	host='127.0.0.1'
	port=8888
	if LOG: open('Log.html', 'w').write("")
	errors = 0
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
		client_socket.connect((host, port))

		for i in range(0, COUNT):
			message = select_random_words("Words.txt", random.randrange(3,8))
			data = encode_hamming(str_to_bits(message))
			crc = crc32_encode(str_to_bits(message))
			noisy_data = hamming_noise(data, NOISE_FACTOR, MULTI_ERROR_FACTOR)

			if LOG: open('Log.html', 'a').write(f"\n<pre>\n[Send] Message: {message}")
			if LOG: open('Log.html', 'a').write(f"\n[Send] Hamming: {list_str(data)}")
			if LOG: open('Log.html', 'a').write(f"\n[Send] Noisy  : {list_str(noisy_data)}")

			client_socket.sendall(list_str(noisy_data).encode() + struct.pack('!I', crc))

			response = client_socket.recv(1024)
			if response:
				data = [int(bit) for bit in str(response[:-4])[2:-1]]
				crc_rec = struct.unpack('!I', response[-4:])[0]
				ham, err = decode_hamming(data, PRINT)
				if LOG: open('Log.html', 'a').write(f"\n<y>[Hamming]</y> Errors: {err}")
				if PRINT: print(f"\033[32m[Hamming]\033[0m Decoded: {list_str(ham)}")
				if LOG: open('Log.html', 'a').write(f"\n<g>[Hamming]</g> Decoded: {list_str(ham)}")
				crc_calc = crc32_encode(ham)
				if crc_rec != crc_calc:
					if PRINT: print(f"\033[31m[CRC32]\033[0m Failed {crc_rec:#10x} != {crc_calc:#10x}")
					if LOG: open('Log.html', 'a').write(f"\n<r>[CRC32]</r> Failed {crc_rec:#10x} != {crc_calc:#10x}")
					errors += 1
				else:
					if PRINT: print(f"\033[32m[CRC32]\033[0m Verified {crc_rec:#10x} == {crc_calc:#10x}")
					if LOG: open('Log.html', 'a').write(f"\n<g>[CRC32]</g> Verified {crc_rec:#10x} == {crc_calc:#10x}")
					if PRINT: print(f"\033[32m[Rec]\033[0m : {bits_to_str(ham)}")
					if LOG: open('Log.html', 'a').write(f"\n<g>[Rec]</g> : {bits_to_str(ham)}")
				if PRINT: print("|------------------------------------------------------------------------------------")
				if LOG: open('Log.html', 'a').write("\n</pre>")
	if LOG:
		open('Log.html', 'a').write("\n<body>")
		existing_content = open('Log.html', 'r').read()
		open('Log.html', 'w').write(
f"""<body>
<style>
* {{
	font-family: 'Roboto', monospace;
	font-size: 15px;
	background: rgb(0,0,0);
	color: rgb(220,220,220);
	border-style: solid;
	border-color: rgb(0,0,0);
	border-width: 0px;
	padding: 0;
	margin: 0;
}}
pre {{
	padding: 30px;
	padding-top: 15px;
	padding-bottom: 15px;
	margin-top: 15px;
	margin-left: 5px;
	margin-right: 5px;
	border-width: 1px;
	border-radius: 10px;
	background: rgb(50,50,50);
	color: rgb(200, 200, 200);
	font-weight: 700;
	tab-size: 4;
	white-space: pre-wrap;
	word-wrap: break-word;
}}
r {{
	background: rgb(50,50,50);
	color: rgb(255,50,50);
}}
g {{
	background: rgb(50,50,50);
	color: rgb(50,255,50);
}}
y {{
	background: rgb(50,50,50);
	color: rgb(255,255,50);
}}
</style>
<pre>
Noise Rate: {NOISE_FACTOR*100}%
Flip Rate : {MULTI_ERROR_FACTOR*100}%
MESSAGE   Count: {COUNT}
<g>SUCCESSES</g> Count: {COUNT - errors}
<r>FAILURES</r>  Count: {errors}
</pre>
""" + existing_content)

if __name__ == '__main__':
	main()