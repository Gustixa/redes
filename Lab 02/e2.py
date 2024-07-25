from typing import *

def calc_paridad(bits: List[int], posiciones: List[int]):
	"""
	Calcula el bit de paridad para las posiciones dadas.

	Args:
		bits (list of int): Lista de bits.
		posiciones (list of int): Lista de posiciones para calcular la paridad.

	Returns:
		int: Bit de paridad calculado.
	"""
	paridad = 0
	for posicion in posiciones:
		paridad ^= int(bits[posicion - 1])
	return paridad

def calc_paridad_bits(data_bits: List[int]):
	"""
	Calcula los bits de paridad y los intercala con los bits de datos.

	Args:
		data_bits (list of int): Lista de bits de datos.

	Returns:
		list of int: Lista de bits con los bits de paridad intercalados.
	"""
	n = len(data_bits)
	m = 0
	while (2 ** m) < (m + n + 1):
		m += 1
		
	encoded_bits = [0] * (n + m)
	j = 0
	for i in range(1, n + m + 1):
		if (i & (i - 1)) == 0:
			continue
		encoded_bits[i - 1] = int(data_bits[j])
		j += 1

	for i in range(m):
		posiciones = []
		for j in range(1, n + m + 1):
			if j & (2 ** i) == (2 ** i):
				posiciones.append(j)
		encoded_bits[(2 ** i) - 1] = calc_paridad(encoded_bits, posiciones)
	
	return encoded_bits

def detect_and_correct_error(encoded_bits: List[int]):
	"""
	Detecta y corrige errores en los bits codificados.

	Args:
		encoded_bits (list of int): Lista de bits codificados.

	Returns:
		tuple: Tupla que contiene los bits corregidos y la posición del error.
	"""
	m = 0
	while (2 ** m) < len(encoded_bits):
		m += 1

	error_posicion = 0
	for i in range(m):
		posiciones = []
		for j in range(1, len(encoded_bits) + 1):
			if j & (2 ** i) == (2 ** i):
				posiciones.append(j)
		if calc_paridad(encoded_bits, posiciones) != 0:
			error_posicion += 2 ** i

	if error_posicion != 0:
		encoded_bits[error_posicion - 1] = '0' if encoded_bits[error_posicion - 1] == '1' else '1'

	return encoded_bits, error_posicion

def decode_hamming(encoded_bits: List[int]):
	"""
	Decodifica los bits codificados usando el código Hamming.

	Args:
		encoded_bits (list of int): Lista de bits codificados.

	Returns:
		list of int: Lista de bits de datos decodificados.
	"""
	corrected_bits, _ = detect_and_correct_error(encoded_bits)
	data_bits = []
	for i in range(1, len(corrected_bits) + 1):
		if (i & (i - 1)) != 0:
			data_bits.append(corrected_bits[i - 1])
	return data_bits

def bits_to_char(bits: List[int]):
	"""
	Convierte una lista de bits en un carácter ASCII.

	Args:
		bits (list of int): Lista de bits.

	Returns:
		str: Carácter ASCII correspondiente.
	"""
	return chr(int(''.join(map(str, bits)), 2))

# Ejemplo de uso para (11, 7)
data_bits_str_11_7 = "1011001"
data_bits_11_7 = [int(bit) for bit in data_bits_str_11_7]

# Calcula los bits de paridad y codifica los bits de datos
encoded_bits_11_7 = calc_paridad_bits(data_bits_11_7)
print(f"(11,7) Bits codificados: {encoded_bits_11_7}")

# Decodifica los bits codificados y detecta/corrige errores
decoded_bits_11_7 = decode_hamming(encoded_bits_11_7)
print(f"(11,7) Bits decodificados: {decoded_bits_11_7}")

# Convierte los bits decodificados a un carácter
char_11_7 = bits_to_char(decoded_bits_11_7)
print(f"(11,7) Carácter decodificado: {char_11_7}\n")

# Ejemplo de uso para (7, 4)
data_bits_str_7_4 = "1011"
data_bits_7_4 = [int(bit) for bit in data_bits_str_7_4]

# Calcula los bits de paridad y codifica los bits de datos
encoded_bits_7_4 = calc_paridad_bits(data_bits_7_4)
print(f"(7,4) Bits codificados: {encoded_bits_7_4}")

# Decodifica los bits codificados y detecta/corrige errores
decoded_bits_7_4 = decode_hamming(encoded_bits_7_4)
print(f"(7,4) Bits decodificados: {decoded_bits_7_4}")

# Convierte los bits decodificados a un carácter
char_7_4 = bits_to_char(decoded_bits_7_4)
print(f"(7,4) Carácter decodificado: {char_7_4}")

# Ejemplo de uso para (15, 11)
data_bits_str_15_11 = "1101011010110"
data_bits_15_11 = [int(bit) for bit in data_bits_str_15_11]

# Calcula los bits de paridad y codifica los bits de datos
encoded_bits_15_11 = calc_paridad_bits(data_bits_15_11)
print(f"(15,11) Bits codificados: {encoded_bits_15_11}")

# Decodifica los bits codificados y detecta/corrige errores
decoded_bits_15_11 = decode_hamming(encoded_bits_15_11)
print(f"(15,11) Bits decodificados: {decoded_bits_15_11}")

# Convierte los bits decodificados a un carácter
char_15_11 = bits_to_char(decoded_bits_15_11)
print(f"(15,11) Caracter decodificado: {char_15_11}")
