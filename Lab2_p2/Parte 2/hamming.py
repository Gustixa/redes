from typing import *
import random

def str_to_bits(string: str):
	byte_data = string.encode()
	bit_list: List[int] = []
	for byte in byte_data:
		bits = f"{byte:08b}"
		bit_list.extend(int(bit) for bit in bits)
	
	return bit_list

def bits_to_str(bit_list: List[int]):
	if len(bit_list) % 8 != 0:
		raise ValueError("Bit list length must be a multiple of 8")
	byte_list = []
	for i in range(0, len(bit_list), 8):
		byte = bit_list[i:i+8]
		byte_int = int(''.join(map(str, byte)), 2)
		byte_list.append(byte_int)
	byte_data = bytes(byte_list)
	return byte_data.decode()

def list_str(list: List[Any]):
	return ''.join(map(str, list))

def flip_bit_with_probability(bit_list: List[int], probability: float):
	list = bit_list
	if not (0.0 <= probability <= 1.0):
		raise ValueError("Probability must be between 0.0 and 1.0")

	for i in range(len(list)):
		if random.random() < probability:
			list[i] = 1 - list[i]

	return list

def bits_to_bytes(bit_list: List[int]):
	if len(bit_list) % 8 != 0:
		raise ValueError("Bit list length must be a multiple of 8")

	byte_list = []
	for i in range(0, len(bit_list), 8):
		byte_bits = bit_list[i:i+8]
		byte = int(''.join(map(str, byte_bits)), 2)
		byte_list.append(byte)
	
	return bytes(byte_list)

def bytes_to_bits(byte_data: bytes):
	bit_list: List[int] = []
	for byte in byte_data:
		bits = f"{byte:08b}"
		bit_list.extend(int(bit) for bit in bits)
	
	return bit_list

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

	encoded: List[int] = [0] * n

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
	
	return encoded

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
		print(f"\033[33m[Hamming]\033[0m Error detected at position {syndrome}")
		encoded[syndrome - 1] ^= 1

	data: List[int] = []
	for i in range(1, n + 1):
		if (i & (i - 1)) != 0:
			data.append(encoded[i - 1])
	
	return data