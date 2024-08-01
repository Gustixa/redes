#include <iostream>
#include <vector>
#include <cstring>
#include <arpa/inet.h>  // For socket functions
#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>
#include <bitset>
#include "crc32.hpp"
#include "hamming.hpp"

using namespace std;

#define PRINT false

void start_server() {
    const char* host = "127.0.0.1";
    int port = 8888;

    int server_socket, client_socket;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_addr_len = sizeof(client_addr);

    server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket == -1) {
        cerr << "Error creating socket" << endl;
        return;
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = inet_addr(host);
    server_addr.sin_port = htons(port);

    if (bind(server_socket, (struct sockaddr*)&server_addr, sizeof(server_addr)) == -1) {
        cerr << "Error binding socket" << endl;
        close(server_socket);
        return;
    }

    if (listen(server_socket, 1) == -1) {
        cerr << "Error listening on socket" << endl;
        close(server_socket);
        return;
    }

    if (PRINT) cout << "Server listening on " << host << ":" << port << endl;

    client_socket = accept(server_socket, (struct sockaddr*)&client_addr, &client_addr_len);
    if (client_socket == -1) {
        cerr << "Error accepting connection" << endl;
        close(server_socket);
        return;
    }

    vector<int> data;
    while (true) {
        char buffer[1024];
        ssize_t bytes_received = recv(client_socket, buffer, sizeof(buffer), 0);
        if (bytes_received <= 0) break;

        vector<int> received_data;
        uint32_t crc_rec;
        if (bytes_received > 4) {
            memcpy(&crc_rec, buffer + bytes_received - 4, sizeof(crc_rec));
            crc_rec = ntohl(crc_rec);

            for (int i = 0; i < bytes_received - 4; ++i) {
                bitset<8> bits(buffer[i]);
                for (int j = 0; j < 8; ++j) {
                    received_data.push_back(bits[j]);
                }
            }

            vector<int> ham = decode_hamming(received_data);
            uint32_t crc_calc = crc32_encode(ham);

            if (crc_rec != crc_calc) {
                if (PRINT) {
                    cout << "\033[31m[CRC32]\033[0m Failed " << hex << crc_rec << " != " << crc_calc << endl;
                }
            } else {
                if (PRINT) {
                    cout << "\033[32m[CRC32]\033[0m Verified " << hex << crc_rec << " == " << crc_calc << endl;
                    cout << "\033[32m[Hamming]\033[0m decoded: " << list_str(ham) << endl;
                    cout << "\033[32m[Rec]\033[0m : " << bits_to_str(ham) << endl;
                }
            }

            if (PRINT) cout << "|------------------------------------------------------------------------------------" << endl;
            string response = list_str(received_data) + to_string(crc_rec);
            send(client_socket, response.c_str(), response.size(), 0);
        }
    }

    close(client_socket);
    close(server_socket);
}

int main() {
    start_server();
    return 0;
}
