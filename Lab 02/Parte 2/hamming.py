from typing import *

def string_to_bit_list(string: str):
	byte_data = string.encode()
	bit_list: List[int] = []
	for byte in byte_data:
		bits = f"{byte:08b}"
		bit_list.extend(int(bit) for bit in bits)
	
	return bit_list

def bit_list_to_string(bit_list: List[int]):
	if len(bit_list) % 8 != 0:
		raise ValueError("Bit list length must be a multiple of 8")
	byte_list = []
	for i in range(0, len(bit_list), 8):
		byte = bit_list[i:i+8]
		byte_int = int(''.join(map(str, byte)), 2)
		byte_list.append(byte_int)
	byte_data = bytes(byte_list)
	return byte_data.decode()

def calculate_redundant_bits(data: List[int]):
	m = len(data)
	r = 0
	while (2 ** r < m + r + 1):
		r += 1
	return r

def encode_hamming(data: List[int]):
	data = list(map(int, data))
	m = len(data)
	r = calculate_redundant_bits(data)
	n = m + r

	encoded = [0] * n

	j = 0
	for i in range(1, n + 1):
		if (i & (i - 1)) == 0:
			continue
		encoded[i - 1] = data[j]
		j += 1

	for i in range(r):
		parity_position = 2 ** i
		parity_value = 0
		for j in range(1, n + 1):
			if j & parity_position:
				parity_value ^= encoded[j - 1]
		encoded[parity_position - 1] = parity_value
	
	return ''.join(map(str, encoded))

def decode_hamming(encoded: List[int]):
	encoded = list(map(int, encoded))
	n = len(encoded)
	r = 0
	while (2 ** r < n + 1):
		r += 1

	syndrome = 0
	for i in range(r):
		parity_position = 2 ** i
		parity_value = 0
		for j in range(1, n + 1):
			if j & parity_position:
				parity_value ^= encoded[j - 1]
		syndrome += parity_value * (2 ** i)

	if syndrome != 0:
		print(f"Error detected at position {syndrome}")
		encoded[syndrome - 1] ^= 1

	data = []
	for i in range(1, n + 1):
		if (i & (i - 1)) != 0:
			data.append(encoded[i - 1])
	
	return ''.join(map(str, data))