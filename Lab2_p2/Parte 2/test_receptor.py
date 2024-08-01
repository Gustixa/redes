import socket
import struct

from crc32 import *
from hamming import *

def start_server(host='127.0.0.1', port=65432):
    """
    Inicia un servidor que escucha conexiones, recibe mensajes codificados, los procesa,
    y envía la respuesta de vuelta.

    Args:
        host (str): La dirección IP del servidor para enlazar. Por defecto es '127.0.0.1'.
        port (int): El número de puerto del servidor para escuchar. Por defecto es 65432.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Servidor escuchando en {host}:{port}")

        conn, addr = server_socket.accept()
        with conn:
            while True:
                response = conn.recv(1024)
                if response:
                    data = [int(bit) for bit in str(response[:-4])[2:-1]]
                    crc_rec = struct.unpack('!I', response[-4:])[0]
                    is_valid_rec = crc32_verify(data, crc_rec)
                    crc_calc = crc32_encode(data)
                    is_valid_calc = crc32_verify(data, crc_calc)
                    
                    try:
                        ham = decode_hamming(data)
                        print(f"\033[32m[Hamming]\033[0m decodificado: {list_str(ham)}")
                    except:
                        print("\033[31m[Hamming]\033[0m Error al decodificar Hamming")
                    
                    try:
                        print(f"\033[32m[Mensaje]\033[0m datos: {bits_to_str(ham)}")
                    except:
                        print("\033[31m[Mensaje]\033[0m Error al decodificar Mensaje")
                    
                    if is_valid_rec and is_valid_calc and crc_rec == crc_calc:
                        print(f"\033[32m[CRC32]\033[0m Verificado")
                    else:
                        print(f"\033[31m[CRC32]\033[0m Fallido")
                        print(f"\033[31m[CRC32]\033[0m Recibido  : {crc_rec:#10x}")
                        print(f"\033[31m[CRC32]\033[0m Calculado: {crc_calc:#10x}")
                    
                    print("|---------------------------------")
                    conn.sendall(list_str(data).encode() + struct.pack('!I', crc_calc))
                else:
                    break

if __name__ == '__main__':
    start_server()
