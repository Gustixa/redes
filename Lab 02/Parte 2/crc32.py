from typing import *

def generate_crc32_table():
	polynomial = 0xEDB88320
	table: List[int] = []
	for i in range(256):
		crc = i
		for j in range(8):
			if (crc & 1) != 0:
				crc = (crc >> 1) ^ polynomial
			else:
				crc >>= 1
		table.append(crc)
	return table

def crc32_encode(data: List[int]) -> int:
	crc32_table = generate_crc32_table()
	crc = 0xFFFFFFFF
	for byte in data:
		crc = crc32_table[(crc ^ byte) & 0xFF] ^ (crc >> 8)
	return crc ^ 0xFFFFFFFF