#include <iostream>
#include <winsock2.h>

#pragma comment(lib, "ws2_32.lib")

int main() {
	WSADATA wsa;
	SOCKET s;
	struct sockaddr_in server;
	const char* message = "Hola desde C++";

	// Inicializar Winsock
	std::cout << "Inicializando Winsock..." << std::endl;
	if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) {
		std::cout << "Fallo en la inicialización de Winsock. Error Code: " << WSAGetLastError() << std::endl;
		return 1;
	}

	// Crear socket
	if ((s = socket(AF_INET, SOCK_STREAM, 0)) == INVALID_SOCKET) {
		std::cout << "No se pudo crear el socket. Error Code: " << WSAGetLastError() << std::endl;
		WSACleanup();
		return 1;
	}

	// Configurar la estructura del servidor
	server.sin_addr.s_addr = inet_addr("127.0.0.1");
	server.sin_family = AF_INET;
	server.sin_port = htons(8888);

	// Conectar al servidor
	if (connect(s, (struct sockaddr*)&server, sizeof(server)) < 0) {
		std::cout << "Conexión fallida. Error Code: " << WSAGetLastError() << std::endl;
		closesocket(s);
		WSACleanup();
		return 1;
	}

	// Enviar mensaje
	if (send(s, message, strlen(message), 0) < 0) {
		std::cout << "Envio fallido. Error Code: " << WSAGetLastError() << std::endl;
		closesocket(s);
		WSACleanup();
		return 1;
	}

	std::cout << "Mensaje enviado: " << message << std::endl;

	closesocket(s);
	WSACleanup();
	return 0;
}