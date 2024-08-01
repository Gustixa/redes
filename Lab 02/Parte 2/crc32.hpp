#include <vector>
#include <cstdint>

using namespace std;

vector<int> convertToVectorInt(const vector<unsigned char>& vec_uchar) {
	vector<int> vec_int;
	vec_int.reserve(vec_uchar.size());
	for (unsigned char c : vec_uchar) {
		vec_int.push_back(static_cast<int>(c));
	}
	return vec_int;
}

vector<int> generate_crc32_table() {
	int polynomial = 0xEDB88320;
	vector<int> table(256);

	for (int i = 0; i < 256; ++i) {
		int crc = i;
		for (int j = 0; j < 8; ++j) {
			if (crc & 1) {
				crc = (crc >> 1) ^ polynomial;
			} else {
				crc >>= 1;
			}
		}
		table[i] = crc;
	}
	return table;
}

int crc32_encode(const vector<int>& data) {
	vector<int> crc32_table = generate_crc32_table();
	int crc = 0xFFFFFFFF;

	for (int byte : data) {
		crc = crc32_table[(crc ^ byte) & 0xFF] ^ (crc >> 8);
	}

	return crc ^ 0xFFFFFFFF;
}