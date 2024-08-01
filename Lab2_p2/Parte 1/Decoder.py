def is_binary_string(data):
	return all(char in '01' for char in data)

def get_parity_value(bits, positions):
	parity = 0
	for pos in positions:
		parity ^= int(bits[pos - 1])
	return parity

def correct_hamming_code(encoded_bits, n, k):
	r = n - k
	error_position = 0

	for i in range(r):
		parity_pos = 2 ** i
		parity = 0

		for j in range(1, n + 1):
			if j & parity_pos:
				parity ^= int(encoded_bits[j - 1])
		error_position += parity * parity_pos

	if error_position != 0:
		error_position -= 1
		corrected_code = list(encoded_bits)
		corrected_code[error_position] = '1' if corrected_code[error_position] == '0' else '0'
		encoded_bits = ''.join(corrected_code)
		print(f"Detected error at position: {error_position + 1}")
		print(f"Corrected bits: {encoded_bits}")
	else:
		print("No errors detected.")

	return encoded_bits

def extract_data_bits(encoded_bits, n, k):
	corrected_bits = correct_hamming_code(encoded_bits, n, k)

	data_bits = ""
	for i in range(n):
		if (i + 1) & i == 0:
			continue  
		data_bits += corrected_bits[i]
	
	return data_bits

encoded_message = input("Enter the encoded message: ")
if is_binary_string(encoded_message):
	n = int(input("Enter the total number of bits (n): "))
	if len(encoded_message) == n:
		k = int(input("Enter the number of data bits (k): "))

		print("Original Corrected message:", extract_data_bits(encoded_message, n, k))
	else:
		print("The total number of bits does not match the length of the entered string.")
else:
	print("Invalid input. Please enter a binary string (0s and 1s only).")