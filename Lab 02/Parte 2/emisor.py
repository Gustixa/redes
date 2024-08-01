import socket
import struct
import matplotlib.pyplot as plt
from sympy import sympify

from crc32 import *
from hamming import *

WORD_MIN_LENGTH = 2
WORD_MAX_LENGTH = 4
NOISE_FACTOR_START = 0
NOISE_FACTOR_END   = 7
NOISE_FACTOR_INC   = 0.1
ERROR_RATE_START = 0
ERROR_RATE_END   = 7
ERROR_RATE_INC   = 0.005
COUNT = 8
PRINT = False
LOG = True

noise_variance: List[Tuple[float, List[Tuple[float, int]]]] = []

def select_random_words(filename):
	return ' '.join(random.sample(open(filename, 'r').read().split(), random.randrange(WORD_MIN_LENGTH, WORD_MAX_LENGTH)))

def main():
	if NOISE_FACTOR_END * NOISE_FACTOR_INC > 1: raise ValueError(f"Noise Out of Range {NOISE_FACTOR_END * NOISE_FACTOR_INC}")
	if ERROR_RATE_END * ERROR_RATE_INC > 1: raise ValueError(f"Error Rate Out of Range {ERROR_RATE_END * ERROR_RATE_INC}")

	host='127.0.0.1'
	port=8888
	if LOG: open('Log.html', 'w').write("")
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
		client_socket.connect((host, port))

		noise_rate = NOISE_FACTOR_START
		while noise_rate <= NOISE_FACTOR_END:
			error_rate = ERROR_RATE_START
			error_variance = []
			while error_rate <= ERROR_RATE_END:
				errors = 0
				for _ in range(0, COUNT):
					message = select_random_words("Words.txt")
					data = encode_hamming(str_to_bits(message))
					crc = crc32_encode(str_to_bits(message))
					noisy_data = hamming_noise(data, sympify(noise_rate * NOISE_FACTOR_INC), sympify(error_rate * ERROR_RATE_INC))
					#if i == MULTI_ERROR_FACTOR_START:
					if LOG :
						open('Log.html', 'a').write(f"\n<pre>\n[Send] Message: {message}")
						open('Log.html', 'a').write(f"\n[Send] Hamming: {list_str(data)}")
						open('Log.html', 'a').write(f"\n[Send] Noisy  : {list_str(noisy_data)}")

					client_socket.sendall(list_str(noisy_data).encode() + struct.pack('!I', crc))

					response = client_socket.recv(8192)
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
				print(f"Error Factor: {str(sympify(error_rate* ERROR_RATE_INC*100)).rstrip('0')}%")
				error_variance.append((str(sympify(error_rate* ERROR_RATE_INC*100)).rstrip('0'), errors))
				error_rate += 1
			print(f"Noise Factor: {str(sympify(noise_rate* NOISE_FACTOR_INC*100)).rstrip('0')}%")
			noise_variance.append((str(sympify(noise_rate* NOISE_FACTOR_INC*100)).rstrip('0'), error_variance))
			noise_rate += 1
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
""")

	for noise_rate, data in noise_variance:
		for error_rate, error in data:
			open('Log.html', 'a').write(f"""
<pre>
Noise Rate: {noise_rate}%
Flip Rate : {error_rate}%
MESSAGE   Count: {COUNT}
<g>SUCCESSES</g> Count: {COUNT - error} {((COUNT-error) / (COUNT))*100}%
<r>FAILURES</r>  Count: {error} {((error) / (COUNT))*100}%
</pre>
""" )
	open('Log.html', 'a').write(existing_content)

main()

plt.figure(figsize=(10, 6))

for (x_value, points) in noise_variance:
	x = [point[0] for point in points]
	y = [point[1] for point in points]
	plt.plot(x, y, marker='o', label=f"Noise {x_value}%")

plt.xlabel('Bit Flip%')
plt.ylabel('Error Rate')
plt.title('Graph of Noise Impact')
plt.legend()
plt.grid(True)
plt.savefig('Plot.png')