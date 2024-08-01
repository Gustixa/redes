import java.io.*;
import java.net.*;
import java.nio.ByteBuffer;
import java.util.*;
import java.util.stream.Collectors;

public class receptor {
    private static final boolean PRINT = false;
    private static final int PORT = 8888;

    public static void main(String[] args) {
        try (ServerSocket serverSocket = new ServerSocket(PORT)) {
            System.out.println("Server listening on port " + PORT);
            
            while (true) {
                try (Socket clientSocket = serverSocket.accept()) {
                    System.out.println("Client connected");

                    InputStream input = clientSocket.getInputStream();
                    OutputStream output = clientSocket.getOutputStream();

                    byte[] buffer = new byte[1024];
                    int bytesRead;

                    while ((bytesRead = input.read(buffer)) != -1) {
                        if (bytesRead > 4) {
                            List<Integer> data = new ArrayList<>();
                            for (int i = 0; i < bytesRead - 4; i++) {
                                data.add(buffer[i] - '0');
                            }

                            ByteBuffer wrapped = ByteBuffer.wrap(buffer, bytesRead - 4, 4);
                            int crcRec = wrapped.getInt();

                            List<Integer> ham = decodeHamming(data);
                            int crcCalc = crc32Encode(ham);

                            if (crcRec != crcCalc) {
                                if (PRINT) {
                                    System.out.printf("\033[31m[CRC32]\033[0m Failed 0x%08x != 0x%08x%n", crcRec, crcCalc);
                                }
                            } else {
                                if (PRINT) {
                                    System.out.printf("\033[32m[CRC32]\033[0m Verified 0x%08x == 0x%08x%n", crcRec, crcCalc);
                                    System.out.printf("\033[32m[Hamming]\033[0m decoded: %s%n", listStr(ham));
                                    System.out.printf("\033[32m[Rec]\033[0m : %s%n", bitsToStr(ham));
                                }
                            }
                            if (PRINT) {
                                System.out.println("|------------------------------------------------------------------------------------");
                            }

                            String response = listStr(data);
                            ByteArrayOutputStream responseStream = new ByteArrayOutputStream();
                            responseStream.write(response.getBytes());
                            responseStream.write(ByteBuffer.allocate(4).putInt(crcRec).array());
                            output.write(responseStream.toByteArray());
                        }
                    }
                } catch (IOException e) {
                    System.err.println("Connection error: " + e.getMessage());
                }
            }
        } catch (IOException e) {
            System.err.println("Server error: " + e.getMessage());
        }
    }

    // Bit manipulation functions
    public static List<Integer> strToBits(String str) {
        List<Integer> bitList = new ArrayList<>();
        for (char ch : str.toCharArray()) {
            String bits = String.format("%8s", Integer.toBinaryString(ch)).replace(' ', '0');
            for (char bit : bits.toCharArray()) {
                bitList.add(bit - '0');
            }
        }
        return bitList;
    }

    public static String bitsToStr(List<Integer> bitList) {
        if (bitList.size() % 8 != 0) {
            throw new IllegalArgumentException("Bit list length must be a multiple of 8");
        }

        StringBuilder result = new StringBuilder();
        for (int i = 0; i < bitList.size(); i += 8) {
            StringBuilder byteString = new StringBuilder();
            for (int j = 0; j < 8; j++) {
                byteString.append(bitList.get(i + j));
            }
            result.append((char) Integer.parseInt(byteString.toString(), 2));
        }
        return result.toString();
    }

    public static String listStr(List<Integer> list) {
        return list.stream().map(String::valueOf).collect(Collectors.joining());
    }

    public static List<Integer> bitNoise(List<Integer> bitList, float probability) {
        Random random = new Random();
        List<Integer> noisyBits = new ArrayList<>(bitList);
        for (int i = 0; i < noisyBits.size(); i++) {
            if (random.nextFloat() < probability) {
                noisyBits.set(i, 1 - noisyBits.get(i));
            }
        }
        return noisyBits;
    }

    public static List<List<Integer>> splitIntoChunks(List<Integer> data, int chunkSize) {
        List<List<Integer>> chunks = new ArrayList<>();
        for (int i = 0; i < data.size(); i += chunkSize) {
            chunks.add(new ArrayList<>(data.subList(i, Math.min(data.size(), i + chunkSize))));
        }
        return chunks;
    }

    public static List<Integer> flattenList(List<List<Integer>> nestedList) {
        return nestedList.stream().flatMap(List::stream).collect(Collectors.toList());
    }

    public static List<Integer> encodeHamming(List<Integer> bits) {
        List<Integer> encoded = new ArrayList<>();
        for (List<Integer> decodedBits : splitIntoChunks(bits, 4)) {
            List<Integer> encodedBits = Arrays.asList(new Integer[7]);
            Collections.fill(encodedBits, 0);

            encodedBits.set(2, decodedBits.get(0));
            encodedBits.set(4, decodedBits.get(1));
            encodedBits.set(5, decodedBits.get(2));
            encodedBits.set(6, decodedBits.get(3));

            encodedBits.set(0, encodedBits.get(2) ^ encodedBits.get(4) ^ encodedBits.get(6));
            encodedBits.set(1, encodedBits.get(2) ^ encodedBits.get(5) ^ encodedBits.get(6));
            encodedBits.set(3, encodedBits.get(4) ^ encodedBits.get(5) ^ encodedBits.get(6));

            encoded.addAll(encodedBits);
        }
        return encoded;
    }

    public static List<Integer> decodeHamming(List<Integer> bits) {
        List<Integer> decoded = new ArrayList<>();
        List<List<Integer>> chunks = splitIntoChunks(bits, 7);
        for (int i = 0; i < chunks.size(); i++) {
            List<Integer> encodedBits = chunks.get(i);

            int p1 = encodedBits.get(0) ^ encodedBits.get(2) ^ encodedBits.get(4) ^ encodedBits.get(6);
            int p2 = encodedBits.get(1) ^ encodedBits.get(2) ^ encodedBits.get(5) ^ encodedBits.get(6);
            int p3 = encodedBits.get(3) ^ encodedBits.get(4) ^ encodedBits.get(5) ^ encodedBits.get(6);

            int errorPosition = (p3 << 2) | (p2 << 1) | p1;

            if (errorPosition != 0) {
                encodedBits.set(errorPosition - 1, 1 - encodedBits.get(errorPosition - 1));
                System.out.printf("\033[33m[Hamming]\033[0m Error detected in chunk [%d] at position [%d]%n", i, errorPosition);
            }

            List<Integer> decodedBits = Arrays.asList(
                    encodedBits.get(2),
                    encodedBits.get(4),
                    encodedBits.get(5),
                    encodedBits.get(6)
            );
            decoded.addAll(decodedBits);
        }
        return decoded;
    }

    public static List<Integer> generateCrc32Table() {
        int polynomial = 0xEDB88320;
        List<Integer> table = new ArrayList<>(256);

        for (int i = 0; i < 256; i++) {
            int crc = i;
            for (int j = 0; j < 8; j++) {
                if ((crc & 1) != 0) {
                    crc = (crc >> 1) ^ polynomial;
                } else {
                    crc >>= 1;
                }
            }
            table.add(crc);
        }
        return table;
    }

    public static int crc32Encode(List<Integer> data) {
        List<Integer> crc32Table = generateCrc32Table();
        int crc = 0xFFFFFFFF;

        for (int byteValue : data) {
            crc = crc32Table.get((crc ^ byteValue) & 0xFF) ^ (crc >> 8);
        }

        return crc ^ 0xFFFFFFFF;
    }

    public static boolean crc32Verify(List<Integer> data, int providedChecksum) {
        int computedChecksum = crc32Encode(data);
        return computedChecksum == providedChecksum;
    }
}
