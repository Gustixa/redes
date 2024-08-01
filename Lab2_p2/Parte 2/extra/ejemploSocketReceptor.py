import socket

class CRC32:
    def crc(self, dividend: str, divisor: str) -> str:
        shift = len(dividend) - len(divisor)

        while shift >= 0:
            dividend = bin(int(dividend, 2) ^ (int(divisor, 2) << shift))[2:]
            shift = len(dividend) - len(divisor)

        if len(dividend) < 16:
            dividend = dividend.zfill(16)

        # print("div" + dividend)
        return dividend


HOST = "127.0.0.1"  # IP, capa de Red. 127.0.0.1 es localhost
PORT = 65432        # Puerto, capa de Transporte

# AF_INET especifica IPv4,
#   tambien hay AF_UNIX para unix sockets y AF_INET6
# SOCK_STREAM especifica TCP,
#   tambien hay SOCK_DGRAM para UDP y otros...
# uso de with, para manejo eficiente de objetos/recursos (llama socket.close() al final)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # bind reserva/asigna tal socket a una IP:puerto especifica
    s.bind((HOST, PORT))
    s.listen()
    # accept() bloquea y deja esperando
    conn, addr = s.accept()
    with conn:
        print(f"Conexion Entrante del proceso {addr}")
        received_data = b''  # Inicializa una variable para almacenar los datos recibidos
        while True:  # en caso se envien mas de 1024 bytes
            # recibir 1024 bytes
            data = conn.recv(1024)
            if not data:
                break  # ya se recibio todo
            received_data += data  # Agrega los datos recibidos a la variable persistente
            # print(f"Recibido: \n{data!r}")  # !r !s !a, repr() str() ascii()
        
        # Aquí puedes trabajar con los datos recibidos después de que la conexión se cierre
        print(f"Todos los datos recibidos: \n{received_data!r}")
        # TODO: realizar operaciones con received_data, guardarlo en un archivo, etc.

        data, checksum, syn, dividend, received_data = "", "", "", "", ""
        padding = 0
        polynomial = "100000100110000010001110110110111"  # De 32 bits

        