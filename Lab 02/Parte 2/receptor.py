import socket

def binary_to_string(binary):
	str_data = ''
	for i in range(0, len(binary), 8):
		byte = binary[i:i+8]
		str_data += chr(int(byte, 2))
	return str_data

def check_crc32(data):
	generator = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1]
	crc_data = data[:len(data)-32] + [0] * 32
	for i in range(len(data) - 32):
		if crc_data[i] == 1:
			for j in range(len(generator)):
				crc_data[i + j] ^= generator[j]
	crc = crc_data[-32:]
	return crc == data[-32:]

def decode_hamming(data):
	n = len(data)
	r = 0
	while (2 ** r < n + 1):
		r += 1

	corrected_data = data.copy()
	error_position = 0

	for i in range(r):
		x = 2 ** i
		sum = 0
		for j in range(1, n + 1):
			if j & x:
				sum ^= corrected_data[j - 1]
		error_position += sum * x

	if error_position:
		corrected_data[error_position - 1] ^= 1

	decoded_data = []
	for i in range(1, n + 1):
		if not (i & (i - 1)) == 0:
			decoded_data.append(corrected_data[i - 1])

	return decoded_data

def main():
	host = '127.0.0.1'
	port = 8888

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))
	s.listen(1)
	print("Esperando conexión...")

	conn, addr = s.accept()
	print(f"Conectado por {addr}")

	data = ""
	while True:
		chunk = conn.recv(4096)
		if not chunk:
			break
		data += chunk.decode()

	binary_data = [int(bit) for bit in data]

	hamming_part = binary_data[:-32]
	crc_part = binary_data[-32:]

	if check_crc32(hamming_part):
		print("CRC32 verificado con éxito.")
		decoded_data = decode_hamming(hamming_part)
		message = binary_to_string(''.join(map(str, decoded_data)))
		print(f"Mensaje recibido: {message}")
	else:
		print("Error en CRC32.")

	conn.close()

if __name__ == "__main__":
	main()