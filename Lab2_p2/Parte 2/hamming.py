from typing import *
import random

def str_to_bits(string: str) -> List[int]:
    """
    Convierte una cadena en una lista de bits.

    Args:
        string (str): La cadena de entrada a convertir.

    Returns:
        List[int]: Una lista de bits que representan la cadena de entrada.
    """
    byte_data = string.encode()
    bit_list: List[int] = []
    for byte in byte_data:
        bits = f"{byte:08b}"
        bit_list.extend(int(bit) for bit in bits)
    
    return bit_list

def bits_to_str(bit_list: List[int]) -> str:
    """
    Convierte una lista de bits en una cadena.

    Args:
        bit_list (List[int]): La lista de bits de entrada a convertir.

    Returns:
        str: La cadena decodificada a partir de la lista de bits.

    Raises:
        ValueError: Si la longitud de la lista de bits no es múltiplo de 8.
    """
    if len(bit_list) % 8 != 0:
        raise ValueError("La longitud de la lista de bits debe ser múltiplo de 8")
    byte_list = []
    for i in range(0, len(bit_list), 8):
        byte = bit_list[i:i+8]
        byte_int = int(''.join(map(str, byte)), 2)
        byte_list.append(byte_int)
    byte_data = bytes(byte_list)
    return byte_data.decode()

def list_str(lista: List[Any]) -> str:
    """
    Convierte una lista de elementos en una sola cadena.

    Args:
        lista (List[Any]): La lista de elementos de entrada a convertir.

    Returns:
        str: Una cadena concatenada de todos los elementos de la lista.
    """
    return ''.join(map(str, lista))

def flip_bit_with_probability(bit_list: List[int], pattern_interval: int, pattern: List[int], probability: float) -> List[int]:
    """
    Invierte bits en una lista de manera aleatoria basada en una probabilidad dada.

    Args:
        bit_list (List[int]): La lista de bits de entrada.
        probability (float): La probabilidad de invertir cada bit (entre 0.0 y 1.0).

    Returns:
        List[int]: La lista de bits con algunos bits potencialmente invertidos.

    Raises:
        ValueError: Si la probabilidad no está entre 0.0 y 1.0.
    """
    if not (0.0 <= probability <= 1.0):
        raise ValueError("La probabilidad debe estar entre 0.0 y 1.0")
    if pattern_interval <= 0:
        raise ValueError("El intervalo debe ser mayor a 0")
    if not pattern:
        raise ValueError("El patrón no debe estar vacío")

    pattern_length = len(pattern)
    if pattern_length != pattern_interval:
        raise ValueError("La longitud del patrón debe ser igual al intervalo")

    noisy_list = bit_list[:]
    
    # Número de bloques que se procesarán
    num_blocks = len(bit_list) // pattern_interval
    
    # Índice para aplicar el patrón
    block_index = int(num_blocks * probability)
    
    for i in range(0, len(noisy_list), pattern_interval):
        # Aplica el patrón a los bloques definidos por la probabilidad
        if block_index > 0:
            for j in range(pattern_length):
                if i + j < len(noisy_list) and pattern[j] == 1:
                    noisy_list[i + j] = 1 - noisy_list[i + j]
            block_index -= 1
    
    return noisy_list

def bits_to_bytes(bit_list: List[int]) -> bytes:
    """
    Convierte una lista de bits en bytes.

    Args:
        bit_list (List[int]): La lista de bits de entrada.

    Returns:
        bytes: Un objeto bytes que representa la lista de bits.

    Raises:
        ValueError: Si la longitud de la lista de bits no es múltiplo de 8.
    """
    if len(bit_list) % 8 != 0:
        raise ValueError("La longitud de la lista de bits debe ser múltiplo de 8")

    byte_list = []
    for i in range(0, len(bit_list), 8):
        byte_bits = bit_list[i:i+8]
        byte = int(''.join(map(str, byte_bits)), 2)
        byte_list.append(byte)
    
    return bytes(byte_list)

def bytes_to_bits(byte_data: bytes) -> List[int]:
    """
    Convierte bytes en una lista de bits.

    Args:
        byte_data (bytes): Los bytes de entrada a convertir.

    Returns:
        List[int]: Una lista de bits que representan los bytes de entrada.
    """
    bit_list: List[int] = []
    for byte in byte_data:
        bits = f"{byte:08b}"
        bit_list.extend(int(bit) for bit in bits)
    
    return bit_list

def calculate_redundant_bits(data: List[int]) -> int:
    """
    Calcula el número de bits redundantes necesarios para la codificación Hamming.

    Args:
        data (List[int]): La lista de bits de datos de entrada.

    Returns:
        int: El número de bits redundantes necesarios.
    """
    m = len(data)
    r = 0
    while (2 ** r < m + r + 1):
        r += 1
    return r

def encode_hamming(data: List[int]) -> List[int]:
    """
    Codifica datos usando el código Hamming.

    Args:
        data (List[int]): La lista de bits de datos de entrada.

    Returns:
        List[int]: La lista de bits codificada con Hamming.
    """
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

def decode_hamming(encoded: List[int]) -> List[int]:
    """
    Decodifica datos codificados con Hamming y corrige errores si es necesario.

    Args:
        encoded (List[int]): La lista de bits codificada con Hamming.

    Returns:
        List[int]: La lista de bits de datos decodificada.
    """
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
