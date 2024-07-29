import socket

HOST = "127.0.0.1"  # IP, capa de Red. 127.0.0.1 es localhost
PORT = 65432        # Puerto, capa de Transporte

# AF_INET especifica IPv4,
#   tambien hay AF_UNIX para unix sockets y AF_INET6
# SOCK_STREAM especifica TCP,
#   tambien hay SOCK_DGRAM para UDP y otros...
#uso de with, para manejo eficiente de objetos/recursos (llama socket.close() al final)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #bind reserva/asigna tal socket a una IP:puerto especifica
    s.bind((HOST, PORT))
    s.listen()
    #accept() bloquea y deja esperando
    conn, addr = s.accept()
    with conn:
        print(f"Conexion Entrante del proceso {addr}")
        while True: #en caso se envien mas de 1024 bytes
            #recibir 1024 bytes
            data = conn.recv(1024)
            if not data:
                break   #ya se recibio todo
            print(f"Recibido: \n{data!r}") #!r !s !a, repr() str() ascii()
            #TODO responder, conn.sendall(resp), etc
            
