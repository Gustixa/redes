#include <iostream>
#include <vector>
#include <string>
#include <stdexcept>
#include <bitset>
#include <random>
#include <arpa/inet.h>
#include <unistd.h>
#include <cstring>
#include "ham.hpp"
#include "crc32.hpp"

#define PORT 8888
#define BUFFER_SIZE 1024

using namespace std;

void start_server() {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int addrlen = sizeof(address);
    char buffer[BUFFER_SIZE] = {0};

    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("bind failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    if (listen(server_fd, 3) < 0) {
        perror("listen");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) {
        perror("accept");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    while (true) {
        int valread = read(new_socket, buffer, BUFFER_SIZE);
        if (valread <= 0) {
            break;
        }

        vector<int> data;
        for (int i = 0; i < valread - 4; ++i) {
            data.push_back(buffer[i] - '0');
        }

        uint32_t crc_rec;
        memcpy(&crc_rec, buffer + valread - 4, sizeof(crc_rec));
        crc_rec = ntohl(crc_rec);

        vector<int> decoded_data = decode_hamming(data);
        uint32_t crc_calc = crc32_encode(decoded_data);

        if (crc_rec != crc_calc) {
            cout << "\033[31m[CRC32]\033[0m Failed " << hex << crc_rec << " != " << crc_calc << dec << endl;
        } else {
            cout << "\033[32m[CRC32]\033[0m Verified " << hex << crc_rec << " == " << crc_calc << dec << endl;
            cout << "\033[32m[Hamming]\033[0m decoded: " << list_str(decoded_data) << endl;
            cout << "\033[32m[Rec]\033[0m : " << bits_to_str(decoded_data) << endl;
        }

        cout << "|------------------------------------------------------------------------------------" << endl;

        string response = list_str(data);
        uint32_t crc_response = htonl(crc_rec);
        write(new_socket, response.c_str(), response.size());
        write(new_socket, &crc_response, sizeof(crc_response));
    }

    close(new_socket);
    close(server_fd);
}

int main() {
    start_server();
    return 0;
}
