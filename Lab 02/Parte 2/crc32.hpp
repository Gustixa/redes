#include <vector>
#include <cstdint>

using namespace std;

vector<uint32_t> generate_crc32_table() {
	uint32_t polynomial = 0xEDB88320;
	vector<uint32_t> table(256);

	for (uint32_t i = 0; i < 256; ++i) {
		uint32_t crc = i;
		for (uint32_t j = 0; j < 8; ++j) {
			if ((crc & 1) != 0) {
				crc = (crc >> 1) ^ polynomial;
			} else {
				crc >>= 1;
			}
		}
		table[i] = crc;
	}

	return table;
}

uint32_t crc32_encode(const vector<int>& data) {
	vector<uint32_t> crc32_table = generate_crc32_table();
	uint32_t crc = 0xFFFFFFFF;
	
	for (const int& non_byte : data) {
		uint8_t byte = static_cast<uint8_t>(non_byte);
		crc = crc32_table[(crc ^ byte) & 0xFF] ^ (crc >> 8);
	}
	
	return crc ^ 0xFFFFFFFF;
}