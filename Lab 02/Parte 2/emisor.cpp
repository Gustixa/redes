#include <winsock2.h>
#include <algorithm>
#include <iostream>
#include <vector>
#include <string>
#include <bitset>
#include <cmath>

#pragma comment(lib, "ws2_32.lib")
#pragma execution_character_set( "utf-8" )


std::vector<int> stringToBinary(const std::string& str);

std::vector<int> calculateHammingCode(const std::vector<int>& data);
std::vector<int> calculateCRC32(const std::vector<int>& data);
std::vector<int> appendCRC32(std::vector<int> data);

int main() {
	WSADATA wsa;
	SOCKET s;
	struct sockaddr_in server;
	const std::string message = "Hola C++";
	
	// Convert message to binary and calculate Hamming code and CRC32
	std::vector<int> binaryMessage = stringToBinary(message);
	std::vector<int> hammingCode = calculateHammingCode(binaryMessage);
	std::vector<int> crc = calculateCRC32(binaryMessage);
	hammingCode.insert(hammingCode.end(), crc.begin(), crc.end());

	// Convert vector of ints to string for sending
	std::string sendMessage;
	for (int bit : hammingCode) {
		sendMessage += std::to_string(bit);
	}

	// Initialize Winsock
	std::cout << "Inicializando Winsock..." << std::endl;
	if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) {
		std::cout << "Fallo en la inicialización de Winsock. Error Code: " << WSAGetLastError() << std::endl;
		return 1;
	}

	// Create socket
	if ((s = socket(AF_INET, SOCK_STREAM, 0)) == INVALID_SOCKET) {
		std::cout << "No se pudo crear el socket. Error Code: " << WSAGetLastError() << std::endl;
		WSACleanup();
		return 1;
	}

	// Configure server structure
	server.sin_addr.s_addr = inet_addr("127.0.0.1");
	server.sin_family = AF_INET;
	server.sin_port = htons(8888);

	// Connect to server
	if (connect(s, (struct sockaddr*)&server, sizeof(server)) < 0) {
		std::cout << "Conexión fallida. Error Code: " << WSAGetLastError() << std::endl;
		closesocket(s);
		WSACleanup();
		return 1;
	}

	// Send message
	if (send(s, sendMessage.c_str(), sendMessage.size(), 0) < 0) {
		std::cout << "Envio fallido. Error Code: " << WSAGetLastError() << std::endl;
		closesocket(s);
		WSACleanup();
		return 1;
	}

	std::cout << "Mensaje enviado: " << sendMessage << std::endl;

	closesocket(s);
	WSACleanup();
	return 0;
}

std::vector<int> calculateCRC32(const std::vector<int>& data) {
	std::vector<int> generator = {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1}; // CRC-32 generator polynomial
	std::vector<int> crcData = data;
	crcData.insert(crcData.end(), 32, 0); // Append 32 zeros

	for (size_t i = 0; i < data.size(); i++) {
		if (crcData[i] == 1) {
			for (size_t j = 0; j < generator.size(); j++) {
				crcData[i + j] ^= generator[j];
			}
		}
	}

	std::vector<int> crc(crcData.end() - 32, crcData.end());
	return crc;
}

std::vector<int> calculateHammingCode(const std::vector<int>& data) {
	int m = data.size();
	int r = 0;

	// Calculate the number of redundant bits
	while ((m + r + 1) > std::pow(2, r)) {
		r++;
	}

	// Initialize hamming code vector with redundant bits as 0
	std::vector<int> hammingCode(m + r, 0);
	int j = 0, k = 0;

	// Position the data bits and redundant bits in the hamming code
	for (int i = 1; i <= m + r; i++) {
		if ((i & (i - 1)) == 0) {
			hammingCode[i - 1] = 0; // Redundant bit positions
		} else {
			hammingCode[i - 1] = data[j];
			j++;
		}
	}

	// Calculate the parity bits
	for (int i = 0; i < r; i++) {
		int x = std::pow(2, i);
		for (int j = 1; j <= m + r; j++) {
			if (j & x) {
				hammingCode[x - 1] = hammingCode[x - 1] ^ hammingCode[j - 1];
			}
		}
	}

	return hammingCode;
}

std::vector<int> stringToBinary(const std::string& str) {
	std::vector<int> binary;
	for (char c : str) {
		for (int i = 7; i >= 0; i--) {
			binary.push_back((c >> i) & 1);
		}
	}
	return binary;
}