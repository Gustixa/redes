import socket
import struct
import matplotlib.pyplot as plt

from crc32 import *
from hamming import *

WORD_MIN_LENGTH = 2
WORD_MAX_LENGTH = 10
NOISE_FACTOR_START = 0.1
NOISE_FACTOR_END   = 0.2
NOISE_FACTOR_INC   = 0.1
MULTI_ERROR_FACTOR_START = 0.01
MULTI_ERROR_FACTOR_END   = 0.07
MULTI_ERROR_FACTOR_INC   = 0.01
COUNT = 100
PRINT = False
LOG = True

noise_variance = []

def select_random_words(filename):
	return ' '.join(random.sample(open(filename, 'r').read().split(), random.randrange(WORD_MIN_LENGTH, WORD_MAX_LENGTH)))

def main():
	host='127.0.0.1'
	port=8888
	if LOG: open('Log.html', 'w').write("")
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
		client_socket.connect((host, port))

		noise_rate = NOISE_FACTOR_START
		while noise_rate < NOISE_FACTOR_END:
			error_rate = MULTI_ERROR_FACTOR_START
			error_variance = []
			while error_rate < MULTI_ERROR_FACTOR_END:
				errors = 0
				for _ in range(0, COUNT):
					message = select_random_words("Words.txt")
					data = encode_hamming(str_to_bits(message))
					crc = crc32_encode(str_to_bits(message))
					noisy_data = hamming_noise(data, NOISE_FACTOR_START, error_rate)
					#if i == MULTI_ERROR_FACTOR_START:
					if LOG :
						open('Log.html', 'a').write(f"\n<pre>\n[Send] Message: {message}")
						open('Log.html', 'a').write(f"\n[Send] Hamming: {list_str(data)}")
						open('Log.html', 'a').write(f"\n[Send] Noisy  : {list_str(noisy_data)}")

					client_socket.sendall(list_str(noisy_data).encode() + struct.pack('!I', crc))

					response = client_socket.recv(1024)
					if response:
						data = [int(bit) for bit in str(response[:-4])[2:-1]]
						crc_rec = struct.unpack('!I', response[-4:])[0]
						ham, err = decode_hamming(data, PRINT)
						#if i == MULTI_ERROR_FACTOR_START:
						if LOG:
							open('Log.html', 'a').write(f"\n<y>[Hamming]</y> Errors: {err}")
							open('Log.html', 'a').write(f"\n<g>[Hamming]</g> Decoded: {list_str(ham)}")
						if PRINT: print(f"\033[32m[Hamming]\033[0m Decoded: {list_str(ham)}")
						crc_calc = crc32_encode(ham)
						if crc_rec != crc_calc:
							#if i == MULTI_ERROR_FACTOR_START:
							if PRINT: print(f"\033[31m[CRC32]\033[0m Failed {crc_rec:#10x} != {crc_calc:#10x}")
							if LOG: open('Log.html', 'a').write(f"\n<r>[CRC32]</r> Failed {crc_rec:#10x} != {crc_calc:#10x}")
							errors += 1
						else:
							#if i == MULTI_ERROR_FACTOR_START:
							if PRINT:
								print(f"\033[32m[CRC32]\033[0m Verified {crc_rec:#10x} == {crc_calc:#10x}")
								print(f"\033[32m[Rec]\033[0m : {bits_to_str(ham)}")
							if LOG:
								open('Log.html', 'a').write(f"\n<g>[CRC32]</g> Verified {crc_rec:#10x} == {crc_calc:#10x}")
								open('Log.html', 'a').write(f"\n<g>[Rec]</g> : {bits_to_str(ham)}")
									
						#if i == MULTI_ERROR_FACTOR_START:
						if PRINT: print("|------------------------------------------------------------------------------------")
						if LOG: open('Log.html', 'a').write("\n</pre>")
				print(f"Error Factor: {error_rate}")
				error_variance.append((error_rate, errors))
				error_rate += MULTI_ERROR_FACTOR_INC
			print(f"Noise Factor: {noise_rate}")
			noise_variance.append(noise_rate, error_variance)
			noise_rate += NOISE_FACTOR_INC
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
""" + '\n'.join([f"""
<pre>
Noise Rate: {noise_rate * 100}%
Flip Rate : {error_rate * 100}%
MESSAGE   Count: {COUNT}
<g>SUCCESSES</g> Count: {COUNT - error} {((COUNT-error) / (COUNT))*100}%
<r>FAILURES</r>  Count: {error} {((error) / (COUNT))*100}%
</pre>
""" for (noise_rate, (error_rate, error)) in noise_variance]) + existing_content)

main()
indices = [(MULTI_ERROR_FACTOR_INC * (i+1)) for i, val in enumerate(noise_variance)]
plt.plot(indices, noise_variance)
plt.show()
