#include <iostream>
#include <vector>
#include <string>
#include <thread>
#include <chrono>
#include <cstring>
#include <winsock2.h>
#include <ws2tcpip.h>

#include "crc32.hpp"
#include "hamming.hpp"

#pragma comment(lib, "ws2_32.lib")
#pragma execution_character_set( "utf-8" )

using namespace std;

const float NOISE_FACTOR = 0.5;

vector<int> str_to_bits(const string &str);
string bits_to_str(const vector<int> &bits);
vector<int> bit_noise(const vector<int> &data, float noise_factor);

void start_client(const string &host = "127.0.0.1", int port = 65432, const string &message = "Hello, World!") {
	WSADATA wsaData;
	int iResult = WSAStartup(MAKEWORD(2, 2), &wsaData);
	if (iResult != 0) {
		cerr << "WSAStartup failed with error: " << iResult << endl;
		return;
	}

	SOCKET client_socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
	if (client_socket == INVALID_SOCKET) {
		cerr << "Socket creation failed with error: " << WSAGetLastError() << endl;
		WSACleanup();
		return;
	}

	sockaddr_in server_address;
	memset(&server_address, 0, sizeof(server_address));
	server_address.sin_family = AF_INET;
	server_address.sin_port = htons(port);
	inet_pton(AF_INET, host.c_str(), &server_address.sin_addr);

	if (connect(client_socket, (sockaddr*)&server_address, sizeof(server_address)) == SOCKET_ERROR) {
		cerr << "Connection failed with error: " << WSAGetLastError() << endl;
		closesocket(client_socket);
		WSACleanup();
		return;
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
}

int main() {
	SetConsoleOutputCP(65001);
	start_client();
	return 0;
}