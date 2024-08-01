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

int main() {
	SetConsoleOutputCP(65001);
	return 0;
}