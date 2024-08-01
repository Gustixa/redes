#include <iostream>
#include <vector>
#include <string>
#include <thread>
#include <chrono>
#include <cstring>
#include <winsock2.h>

#include "crc32.hpp"
#include "hamming.hpp"

#pragma comment(lib, "ws2_32.lib")
#pragma execution_character_set( "utf-8" )

using namespace std;

const float NOISE_FACTOR = 0.5;

int main() {
	SetConsoleOutputCP(65001);
	WSADATA wsa;
	SOCKET client_socket;
	struct sockaddr_in server;
	const std::string message = "Hola C++";

	std::cout << "Inicializando Winsock..." << std::endl;
	if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) {
		std::cout << "Fallo en la inicialización de Winsock. Error Code: " << WSAGetLastError() << std::endl;
		return 1;
	}

	if ((client_socket = socket(AF_INET, SOCK_STREAM, 0)) == INVALID_SOCKET) {
		std::cout << "No se pudo crear el socket. Error Code: " << WSAGetLastError() << std::endl;
		WSACleanup();
		return 1;
	}

	server.sin_addr.s_addr = inet_addr("127.0.0.1");
	server.sin_family = AF_INET;
	server.sin_port = htons(8888);

	if (connect(client_socket, (struct sockaddr*)&server, sizeof(server)) < 0) {
		std::cout << "Conexión fallida. Error Code: " << WSAGetLastError() << std::endl;
		closesocket(client_socket);
		WSACleanup();
		return 1;
	}

	while (true) {
		vector<int> data = encode_hamming(str_to_bits(message));
		int crc = crc32_encode(data);
		vector<int> noisy_data = bit_noise(data, NOISE_FACTOR);

		string data_str(noisy_data.begin(), noisy_data.end());
		send(client_socket, data_str.c_str(), data_str.size(), 0);
		send(client_socket, reinterpret_cast<char*>(&crc), sizeof(crc), 0);

		char buffer[1024];
		int received = recv(client_socket, buffer, sizeof(buffer), 0);
		if (received > 0) {
			vector<int> response_data(buffer, buffer + received - 4);
			int crc_rec;
			memcpy(&crc_rec, buffer + received - 4, 4);
			int crc_calc = crc32_encode(response_data);

			bool is_valid_calc = crc32_verify(response_data, crc_calc);
			bool is_valid_rec = crc32_verify(response_data, crc_rec);

			try {
				vector<int> ham = decode_hamming(response_data);
				cout << "\033[32m[Hamming]\033[0m decoded: " << bits_to_str(ham) << endl;
			} catch (const exception &e) {
				cout << "\033[31m[Hamming]\033[0m Failed to decode Hamming [" << e.what() << "]\n";
			}

			try {
				cout << "\033[32m[Message]\033[0m data: " << bits_to_str(response_data) << endl;
			} catch (const exception &e) {
				cout << "\033[31m[Message]\033[0m Failed to decode Message [" << e.what() << "]\n";
			}

			if (is_valid_rec && is_valid_calc && crc_rec == crc_calc) {
				cout << "\033[32m[CRC32]\033[0m Verified\n";
			} else {
				cout << "\033[31m[CRC32]\033[0m Failed\n";
				cout << "\033[31m[CRC32]\033[0m Received  : " << hex << crc_rec << "\n";
				cout << "\033[31m[CRC32]\033[0m Calculated: " << hex << crc_calc << "\n";
			}
			cout << "|---------------------------------\n";
		}

		this_thread::sleep_for(chrono::milliseconds(2500));
	}

	closesocket(client_socket);
	WSACleanup();
	return 0;
}