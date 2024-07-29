#include <iostream>
#include <winsock2.h>
#include <bitset>
#include <vector>
#include <string>
#pragma comment(lib, "ws2_32.lib")

using namespace std;

string decodeMessage(const string& binaryMessage);
bool verifyChecksum(const string& binaryMessage);

int main() {
	WSADATA wsaData;
	SOCKET serverSocket, clientSocket;
	struct sockaddr_in serverAddr, clientAddr;
	int addrLen = sizeof(clientAddr);

	// Inicializar Winsock
	if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
		cerr << "WSAStartup failed.\n";
		return 1;
	}

	// Crear socket
	serverSocket = socket(AF_INET, SOCK_STREAM, 0);
	if (serverSocket == INVALID_SOCKET) {
		cerr << "Socket creation failed.\n";
		WSACleanup();
		return 1;
	}

	// Configurar dirección del servidor
	serverAddr.sin_family = AF_INET;
	serverAddr.sin_addr.s_addr = INADDR_ANY;
	serverAddr.sin_port = htons(8080);

	// Enlazar socket
	if (bind(serverSocket, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
		cerr << "Bind failed.\n";
		closesocket(serverSocket);
		WSACleanup();
		return 1;
	}

	// Escuchar conexiones
	if (listen(serverSocket, 5) == SOCKET_ERROR) {
		cerr << "Listen failed.\n";
		closesocket(serverSocket);
		WSACleanup();
		return 1;
	}

	cout << "Esperando conexiones...\n";

	// Aceptar conexión
	clientSocket = accept(serverSocket, (struct sockaddr*)&clientAddr, &addrLen);
	if (clientSocket == INVALID_SOCKET) {
		cerr << "Accept failed.\n";
		closesocket(serverSocket);
		WSACleanup();
		return 1;
	}

	cout << "Cliente conectado.\n";

	// Recibir datos del cliente
	char buffer[1024];
	int bytesReceived = recv(clientSocket, buffer, sizeof(buffer), 0);
	if (bytesReceived > 0) {
		string binaryMessage(buffer, bytesReceived);

		// Verificar y decodificar el mensaje
		if (verifyChecksum(binaryMessage)) {
			string message = decodeMessage(binaryMessage);
			cout << "Mensaje recibido y decodificado: " << message << "\n";
		} else {
			cerr << "Error en la integridad del mensaje.\n";
		}
	}

	// Cerrar sockets
	closesocket(clientSocket);
	closesocket(serverSocket);
	WSACleanup();
	return 0;
}

string decodeMessage(const string& binaryMessage) {
	string message;
	for (size_t i = 0; i < binaryMessage.size(); i += 8) {
		bitset<8> byte(binaryMessage.substr(i, 8));
		message += static_cast<char>(byte.to_ulong());
	}
	return message;
}

bool verifyChecksum(const string& binaryMessage) {
	// Implementación básica de verificación de checksum
	int sum = 0;
	for (size_t i = 0; i < binaryMessage.size(); i += 8) {
		bitset<8> byte(binaryMessage.substr(i, 8));
		sum += byte.to_ulong();
	}
	return (sum % 256) == 0;
}