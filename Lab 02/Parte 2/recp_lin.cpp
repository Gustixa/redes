#include <iostream>
#include <vector>
#include <string>
#include <cstring>
#include <unistd.h>
#include <arpa/inet.h>
#include "crc32.hpp"
#include "hamming.hpp"

using namespace std;

void start_server() {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    const int port = 8888;
    const bool PRINT = false;

    // Creating socket file descriptor
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    // Forcefully attaching socket to the port 8888
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) {
        perror("setsockopt");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(port);

    // Forcefully attaching socket to the port 8888
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

    cout << "Server listening on port " << port << endl;

    if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) {
        perror("accept");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    const int recvbuflen = 1024;
    char recvbuf[recvbuflen];

    // Receive until the peer shuts down the connection
    int iResult;
    do {
        iResult = recv(new_socket, recvbuf, recvbuflen, 0);
        if (iResult > 0) {
            cout << "Bytes received: " << iResult << endl;

            vector<int> data;
            for (int i = 0; i < iResult - 4; i++) {
                data.push_back(recvbuf[i] - '0');
            }

            uint32_t crc_rec;
            memcpy(&crc_rec, recvbuf + iResult - 4, 4);

            vector<int> ham;
            int err;
            tie(ham, err) = decode_hamming(data, PRINT);

            uint32_t crc_calc = crc32_encode(ham);

            if (crc_rec != crc_calc) {
                cout << "\033[31m[CRC32]\033[0m Failed " << hex << crc_rec << " != " << crc_calc << dec << endl;
            } else {
                if (PRINT) {
                    cout << "\033[32m[CRC32]\033[0m Verified " << hex << crc_rec << " == " << crc_calc << dec << endl;
                    cout << "\033[32m[Hamming]\033[0m decoded: " << list_str(ham) << endl;
                    cout << "\033[32m[Rec]\033[0m : " << bits_to_str(ham) << endl;
                }
            }
            cout << "|------------------------------------------------------------------------------------" << endl;

            string response = list_str(data);
            response += string(reinterpret_cast<char*>(&crc_rec), 4);
            send(new_socket, response.c_str(), response.size(), 0);

        } else if (iResult == 0) {
            cout << "Connection closing..." << endl;
        } else {
            perror("recv failed");
            close(new_socket);
            close(server_fd);
            exit(EXIT_FAILURE);
        }
    } while (iResult > 0);

    // Shutdown the connection since we're done
    if (shutdown(new_socket, SHUT_RDWR) < 0) {
        perror("shutdown failed");
        close(new_socket);
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    // Cleanup
    close(new_socket);
    close(server_fd);
}

int main() {
    start_server();
    return 0;
}
