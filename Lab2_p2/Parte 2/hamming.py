from typing import *
import random

def str_to_bits(string: str) -> List[int]:
    """
    Convertir una cadena en una lista de bits.

    Args:
        string (str): La cadena de entrada a convertir.

    Returns:
        List[int]: Una lista de bits que representa la cadena de entrada.
    """
    byte_data = string.encode()
    bit_list: List[int] = []
    for byte in byte_data:
        bits = f"{byte:08b}"
        bit_list.extend(int(bit) for bit in bits)
    return bit_list

def bits_to_str(bit_list: List[int]) -> str:
    """
    Convertir una lista de bits en una cadena.

    Args:
        bit_list (List[int]): La lista de bits de entrada a convertir.

    Returns:
        str: La cadena decodificada de la lista de bits.

    Raises:
        ValueError: Si la longitud de la lista de bits no es múltiplo de 8.
    """
    if len(bit_list) % 8 != 0:
        raise ValueError("La longitud de la lista de bits debe ser un múltiplo de 8")
    byte_list = []
    for i in range(0, len(bit_list), 8):
        byte = bit_list[i:i+8]
        byte_int = int(''.join(map(str, byte)), 2)
        byte_list.append(byte_int)
    byte_data = bytes(byte_list)
    return byte_data.decode()

def list_str(lst: List[Any]) -> str:
    """
    Convertir una lista de elementos en una sola cadena.

    Args:
        lst (List[Any]): La lista de elementos de entrada a convertir.

    Returns:
        str: Una cadena concatenada de todos los elementos de la lista.
    """
    return ''.join(map(str, lst))

def flip_bit_with_probability(bit_list: List[int], probability: float) -> List[int]:
    """
    Cambiar aleatoriamente bits en una lista basada en una probabilidad dada.

    Args:
        bit_list (List[int]): La lista de bits de entrada.
        probability (float): La probabilidad de cambiar cada bit (entre 0.0 y 1.0).

    Returns:
        List[int]: La lista de bits con algunos bits potencialmente cambiados.

    Raises:
        ValueError: Si la probabilidad no está entre 0.0 y 1.0.
    """
    if not (0.0 <= probability <= 1.0):
        raise ValueError("La probabilidad debe estar entre 0.0 y 1.0")

    noisy_list = bit_list[:]
    for i in range(len(noisy_list)):
        if random.random() < probability:
            noisy_list[i] = 1 - noisy_list[i]

    return noisy_list

def bits_to_bytes(bit_list: List[int]) -> bytes:
    """
    Convertir una lista de bits en bytes.

    Args:
        bit_list (List[int]): La lista de bits de entrada.

    Returns:
        bytes: Un objeto bytes que representa la lista de bits.

    Raises:
        ValueError: Si la longitud de la lista de bits no es múltiplo de 8.
    """
    if len(bit_list) % 8 != 0:
        raise ValueError("La longitud de la lista de bits debe ser un múltiplo de 8")

    byte_list = []
    for i in range(0, len(bit_list), 8):
        byte_bits = bit_list[i:i+8]
        byte = int(''.join(map(str, byte_bits)), 2)
        byte_list.append(byte)
    return bytes(byte_list)

def bytes_to_bits(byte_data: bytes) -> List[int]:
    """
    Convertir bytes en una lista de bits.

    Args:
        byte_data (bytes): Los bytes de entrada a convertir.

    Returns:
        List[int]: Una lista de bits que representa los bytes de entrada.
    """
    bit_list: List[int] = []
    for byte in byte_data:
        bits = f"{byte:08b}"
        bit_list.extend(int(bit) for bit in bits)
    return bit_list

def calculate_redundant_bits(data: List[int]) -> int:
    """
    Calcular el número de bits redundantes necesarios para la codificación Hamming.

    Args:
        data (List[int]): La lista de bits de datos de entrada.

    Returns:
        int: El número de bits redundantes requeridos.
    """
    m = len(data)
    r = 0
    while (2 ** r < m + r + 1):
        r += 1
    return r

def encode_hamming(data: List[int]) -> List[int]:
    """
    Codificar datos utilizando el código Hamming.

    Args:
        data (List[int]): La lista de bits de datos de entrada.

    Returns:
        List[int]: La lista de bits codificados con Hamming.
    """
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
    Decodificar datos codificados con Hamming y corregir errores si es necesario.

    Args:
        encoded (List[int]): La lista de bits codificados con Hamming de entrada.

    Returns:
        List[int]: La lista de bits de datos decodificados.
    """
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
