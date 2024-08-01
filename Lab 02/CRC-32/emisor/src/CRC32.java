import java.math.BigInteger;

public class CRC32 {
    private static final String POLYNOMIAL = "100000100110000010001110110110111";

    public static String calculateCRC(String data) {
        String dividend = data + "0".repeat(32);
        BigInteger dividendInt = new BigInteger(dividend, 2);
        BigInteger divisorInt = new BigInteger(POLYNOMIAL, 2);
        int shift = dividend.length() - POLYNOMIAL.length();

        while (shift >= 0) {
            dividendInt = dividendInt.xor(divisorInt.shiftLeft(shift));
            shift = dividendInt.bitLength() - divisorInt.bitLength();
        }

        String crc = dividendInt.toString(2);
        return String.format("%32s", crc).replace(' ', '0'); // Padding to 32 bits
    }

    public static void main(String[] args) {
        // String data = "1010101111001101"; // Example data
        // String data = "110010101111";
        String data = "100110111";
        String crc = calculateCRC(data);
        String transmittedData = data + crc;
        System.out.println("CRC generated: " + crc);
        System.out.println("Codeword transmitted: " + transmittedData);
    }
}
