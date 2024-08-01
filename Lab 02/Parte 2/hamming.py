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

def split_into_chunks(data: List[int], chunk_size: int = 4) -> List[List[int]]:
	return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

def flatten_list(nested_list: List[List[Any]]) -> List[Any]:
	return [item for sublist in nested_list for item in sublist]

def hamming_noise(bit_list: List[int], factor: float, multi_error: int) -> List[int]:
	noisy_bits: List[int] = []
	for bit_sequence in split_into_chunks(bit_list, 7):
		sequence = bit_sequence
		if random.random() < factor:
			error_index = random.randint(0, 6)
			sequence[error_index] = 1 - bit_sequence[error_index]

		for i in range(7):
			if random.random() < multi_error:
				sequence[i] = 1 - sequence[i]

		noisy_bits.append(sequence)

	return flatten_list(noisy_bits)

def encode_hamming(bits: List[int]) -> List[int]:
	encoded = []
	for decoded_bits in split_into_chunks(bits, 4):
		encoded_bits = [0] * 7

		encoded_bits[2] = decoded_bits[0]
		encoded_bits[4] = decoded_bits[1]
		encoded_bits[5] = decoded_bits[2]
		encoded_bits[6] = decoded_bits[3]

		encoded_bits[0] = encoded_bits[2] ^ encoded_bits[4] ^ encoded_bits[6]
		encoded_bits[1] = encoded_bits[2] ^ encoded_bits[5] ^ encoded_bits[6]
		encoded_bits[3] = encoded_bits[4] ^ encoded_bits[5] ^ encoded_bits[6]

		encoded.append(encoded_bits)
	return flatten_list(encoded)

def decode_hamming(bits: List[int], PRINT: bool) -> List[int]:
	decoded = []
	errors = []
	for encoded_bits in split_into_chunks(bits, 7):
		p1 = encoded_bits[0] ^ encoded_bits[2] ^ encoded_bits[4] ^ encoded_bits[6]
		p2 = encoded_bits[1] ^ encoded_bits[2] ^ encoded_bits[5] ^ encoded_bits[6]
		p3 = encoded_bits[3] ^ encoded_bits[4] ^ encoded_bits[5] ^ encoded_bits[6]

		error = [0] * 7
		error_position = (p3 << 2) | (p2 << 1) | p1

		if error_position != 0:
			encoded_bits[error_position - 1] ^= 1
			error[error_position - 1] = 1

		decoded_bits = [encoded_bits[2], encoded_bits[4], encoded_bits[5], encoded_bits[6]]

		decoded.append(decoded_bits)
		errors.append(error)

	error_flatten = flatten_list(errors)
	error_list = ''.join([f'\033[31m{bit}\033[0m' if error_flatten[i] else str(bit) for i, bit in enumerate(bits)])
	if PRINT: print(f"\033[33m[Hamming]\033[0m Errors: {error_list}")
	error_list = ''.join([f'<r>{bit}</r>' if error_flatten[i] else str(bit) for i, bit in enumerate(bits)])
	return flatten_list(decoded), error_list