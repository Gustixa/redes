#include <iostream>
#include <cstring>
#include <sstream>
#include <chrono>
#include <string>
#include <thread>
#include <vector>
#include <bitset>

#include <winsock2.h>
#include <ws2tcpip.h>

#include "crc32.hpp"
#include "hamming.hpp"

#pragma comment(lib, "ws2_32.lib")
#pragma execution_character_set( "utf-8" )

using namespace std;

const bool PRINT = false;

int main() {
	SetConsoleOutputCP(CP_UTF8);
	const int PORT = 8888;
	const char* HOST = "127.0.0.1";

	WSADATA wsaData;
	SOCKET server_socket, client_socket;
	struct sockaddr_in server_addr, client_addr;
	int client_addr_len = sizeof(client_addr);

	if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
		cerr << "WSAStartup failed." << endl;
		return 1;
	}

	server_socket = socket(AF_INET, SOCK_STREAM, 0);
	if (server_socket == INVALID_SOCKET) {
		cerr << "Socket creation failed." << endl;
		WSACleanup();
		return 1;
	}

	server_addr.sin_family = AF_INET;
	server_addr.sin_port = htons(PORT);
	inet_pton(AF_INET, HOST, &server_addr.sin_addr);

	if (bind(server_socket, (struct sockaddr*)&server_addr, sizeof(server_addr)) == SOCKET_ERROR) {
		cerr << "Bind failed." << endl;
		closesocket(server_socket);
		WSACleanup();
		return 1;
	}

	if (listen(server_socket, SOMAXCONN) == SOCKET_ERROR) {
		cerr << "Listen failed." << endl;
		closesocket(server_socket);
		WSACleanup();
		return 1;
	}

	if (PRINT) {
		cout << "Server listening on " << HOST << ":" << PORT << endl;
	}

	client_socket = accept(server_socket, (struct sockaddr*)&client_addr, &client_addr_len);
	if (client_socket == INVALID_SOCKET) {
		cerr << "Accept failed." << endl;
		closesocket(server_socket);
		WSACleanup();
		return 1;
	}

	char buffer[1024];
	int bytes_received;
	while ((bytes_received = recv(client_socket, buffer, 1024, 0)) > 0) {
		vector<int> data;
		try {
				for (int i = 0; i < bytes_received - 4; ++i) {
				data.push_back(buffer[i] - '0');
			}

			uint32_t crc_rec = ntohl(*reinterpret_cast<uint32_t*>(buffer + bytes_received - 4));
			auto [ham, err] = decode_hamming(data, PRINT);
			if (PRINT) {
				cout << "\033[32m[Hamming]\033[0m Decoded: " << list_str(data) << endl;
			}
			uint32_t crc_calc = crc32_encode(ham);

			if (crc_rec != crc_calc) {
				if (PRINT) {
					cerr << "\033[31m[CRC32]\033[0m Failed " << hex << crc_rec << " != " << crc_calc << endl;
				}
			} else {
				if (PRINT) {
					cout << "\033[32m[CRC32]\033[0m Verified " << hex << crc_rec << " == " << crc_calc << endl;
					cout << "\033[32m[Rec]\033[0m : " << bits_to_str(ham) << endl;
				}
			}
			if (PRINT) {
				cout << "|------------------------------------------------------------------------------------" << endl;
			}
		}
		catch (exception e) {
			cerr << e.what() << endl;
		}
		send (client_socket, buffer, bytes_received, 0);
	}

	closesocket(client_socket);
	closesocket(server_socket);
	WSACleanup();

	return 0;
}