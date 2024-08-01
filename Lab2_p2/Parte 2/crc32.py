from typing import *

def generate_crc32_table() -> List[int]:
    """
    Genera una tabla de búsqueda CRC32 usando el polinomio 0xEDB88320.

    Returns:
        List[int]: Una lista de 256 enteros que representan la tabla de búsqueda CRC32.
    """
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
    """
    Calcula el checksum CRC32 para una lista de bytes de datos dada.

    Args:
        data (List[int]): Una lista de enteros que representan los bytes de datos.

    Returns:
        int: El checksum CRC32 de los datos de entrada.
    """
    crc32_table = generate_crc32_table()
    crc = 0xFFFFFFFF
    for byte in data:
        crc = crc32_table[(crc ^ byte) & 0xFF] ^ (crc >> 8)
    return crc ^ 0xFFFFFFFF

def crc32_verify(data: List[int], provided_checksum: int) -> bool:
    """
    Verifica si el checksum CRC32 proporcionado coincide con el checksum calculado para los datos dados.

    Args:
        data (List[int]): Una lista de enteros que representan los bytes de datos.
        provided_checksum (int): El checksum CRC32 a verificar.

    Returns:
        bool: True si el checksum proporcionado coincide con el checksum calculado, False en caso contrario.
    """
    computed_checksum = crc32_encode(data)
    return computed_checksum == provided_checksum
