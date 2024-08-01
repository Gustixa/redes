#include <iostream>
#include <vector>
#include <cmath>
#include <string>
#include <algorithm>

using namespace std;

// Function to calculate the parity bit
int calculateParity(const vector<int>& bits, const vector<int>& positions) {
	int parity = 0;
	for (int pos : positions) {
		parity ^= bits[pos - 1];
	}
	return parity;
}

// Function to encode data using Hamming (n, k)
string encodeHamming(const string& data, int n, int k) {
	int r = n - k;
	vector<int> bits(n, 0);
	vector<int> dataBitPositions;

	// Determine positions for data and parity bits
	for (int i = 1, j = 0; i <= n; i++) {
		if ((i & (i - 1)) != 0) {
			dataBitPositions.push_back(i - 1);
		}
	}

	// Insert data bits into their positions
	for (size_t i = 0; i < data.length(); i++) {
		bits[dataBitPositions[i]] = data[i] - '0';
	}

	// Calculate parity bits
	for (int i = 0; i < r; i++) {
		int parityPosition = static_cast<int>(pow(2, i));
		vector<int> parityPositions;
		for (int j = 1; j <= n; j++) {
			if (((j >> i) & 1) == 1) {
				parityPositions.push_back(j);
			}
		}
		bits[parityPosition - 1] = calculateParity(bits, parityPositions);
	}

	// Convert bits vector to a binary string
	string encodedMessage;
	for (int bit : bits) {
		encodedMessage += to_string(bit);
	}

	return encodedMessage;
}

string modifyMessage(const string& encodedMessage) {
	string modifiedMessage = encodedMessage;
	modifiedMessage[0] = modifiedMessage[0] == '0' ? '1' : '0';
	modifiedMessage[1] = modifiedMessage[1] == '0' ? '1' : '0';
	return modifiedMessage;
}

int main() {
	int n, k;
	cout << "Enter the total number of bits (n): ";
	cin >> n;
	cout << "Enter the number of data bits (k): ";
	cin >> k;

	cin.ignore(); // Ignore the newline character after reading k

	string message;
	cout << "Enter a binary message of " << k << " bits: ";
	getline(cin, message);

	if (message.length() != k) {
		cout << "The message must be exactly " << k << " bits." << endl;
		return 1;
	}

	string encodedMessage = encodeHamming(message, n, k);
	cout << "Encoded message: " << encodedMessage << endl;

	string modifiedMessage = modifyMessage(message);
	cout << "Modified message: " << modifiedMessage << endl;

	return 0;
}
