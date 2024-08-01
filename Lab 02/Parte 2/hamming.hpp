#include <iostream>
#include <vector>
#include <string>
#include <stdexcept>
#include <random>
#include <bitset>

using namespace std;

vector<int> str_to_bits(const string &str) {
	vector<int> bit_list;
	for (char ch : str) {
		bitset<8> bits(ch);
		for (size_t i = 0; i < 8; ++i) {
			bit_list.push_back(bits[i]);
		}
	}
	return bit_list;
}

string bits_to_str(const vector<int> &bit_list) {
	if (bit_list.size() % 8 != 0) {
		throw invalid_argument("Bit list length must be a multiple of 8");
	}

	string result;
	for (size_t i = 0; i < bit_list.size(); i += 8) {
		bitset<8> bits;
		for (size_t j = 0; j < 8; ++j) {
			bits[j] = bit_list[i + j];
		}
		result += static_cast<char>(bits.to_ulong());
	}
	return result;
}

string list_str(const vector<int> &list) {
	string result;
	for (int element : list) {
		result += to_string(element);
	}
	return result;
}

vector<int> bit_noise(const vector<int> &bit_list, float probability) {
	random_device rd;
	mt19937 gen(rd());
	uniform_real_distribution<> dis(0, 1);

	vector<int> noisy_bits = bit_list;
	for (auto &bit : noisy_bits) {
		if (dis(gen) < probability) {
			bit = 1 - bit;
		}
	}
	return noisy_bits;
}

vector<vector<int>> split_into_chunks(const vector<int> &data, int chunk_size) {
	vector<vector<int>> chunks;
	for (size_t i = 0; i < data.size(); i += chunk_size) {
		vector<int> chunk(data.begin() + i, data.begin() + min(data.size(), i + chunk_size));
		chunks.push_back(chunk);
	}
	return chunks;
}

vector<int> flatten_list(const vector<vector<int>> &nested_list) {
	vector<int> flat_list;
	for (const auto &sublist : nested_list) {
		flat_list.insert(flat_list.end(), sublist.begin(), sublist.end());
	}
	return flat_list;
}

vector<int> encode_hamming(const vector<int> &bits) {
	vector<int> encoded;
	for (const auto &decoded_bits : split_into_chunks(bits, 4)) {
		vector<int> encoded_bits(7);

		encoded_bits[2] = decoded_bits[0];
		encoded_bits[4] = decoded_bits[1];
		encoded_bits[5] = decoded_bits[2];
		encoded_bits[6] = decoded_bits[3];

		encoded_bits[0] = encoded_bits[2] ^ encoded_bits[4] ^ encoded_bits[6];
		encoded_bits[1] = encoded_bits[2] ^ encoded_bits[5] ^ encoded_bits[6];
		encoded_bits[3] = encoded_bits[4] ^ encoded_bits[5] ^ encoded_bits[6];

		encoded.insert(encoded.end(), encoded_bits.begin(), encoded_bits.end());
	}
	return encoded;
}

vector<int> decode_hamming(const vector<int> &bits) {
	vector<int> decoded;
	auto chunks = split_into_chunks(bits, 7);
	for (size_t i = 0; i < chunks.size(); ++i) {
		auto encoded_bits = chunks[i];

		int p1 = encoded_bits[0] ^ encoded_bits[2] ^ encoded_bits[4] ^ encoded_bits[6];
		int p2 = encoded_bits[1] ^ encoded_bits[2] ^ encoded_bits[5] ^ encoded_bits[6];
		int p3 = encoded_bits[3] ^ encoded_bits[4] ^ encoded_bits[5] ^ encoded_bits[6];

		int error_position = (p3 << 2) | (p2 << 1) | p1;

		if (error_position != 0) {
			encoded_bits[error_position - 1] ^= 1;
			cout << "\033[33m[Hamming]\033[0m Error detected in chunk [" << i << "] at position [" << error_position << "]\n";
		}

		vector<int> decoded_bits = {encoded_bits[2], encoded_bits[4], encoded_bits[5], encoded_bits[6]};
		decoded.insert(decoded.end(), decoded_bits.begin(), decoded_bits.end());
	}
	return decoded;
}