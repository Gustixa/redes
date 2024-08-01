//Sockets en Java - Emisor
//Miguel Novella - Redes UVG - 2023

//Para TCP usar Socket, para UDP DatagramSocket
//En versiones anteriores de java todo era via Socket(stream/datagram)
//para recibir se usar ServerSocket
import java.net.Socket;
import java.net.InetAddress;
//input stream reader para leer
import java.io.OutputStreamWriter;
import java.math.BigInteger;
import java.io.IOException;		//exceptions
import java.net.UnknownHostException;
import java.math.BigInteger;
import java.util.Scanner;

public class Emisor{

	private static String HOST = "127.0.0.1";	//a.k.a. localhost, o loopback
	private static int PORT = 65432;		//elegir puerto
	private static final String POLYNOMIAL = "100000100110000010001110110110111";
	
	/**
	 * 
	 * @param data
	 * @return
	 */
    private static String calculateCRC(String data) {
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

	/**
	 * 
	 * @param texto
	 * @return
	 */
	private static String string_to_bin(String texto){
		StringBuilder binarios = new StringBuilder();

        for (char ch : texto.toCharArray()) {
            // Obtener el valor ASCII del carácter
            int valorAscii = (int) ch;
            
            // Convertir el valor ASCII a binario y asegurar que tenga 8 bits
            String valorBinario = String.format("%8s", Integer.toBinaryString(valorAscii)).replace(' ', '0');
            
            // Añadir el valor binario al resultado
            binarios.append(valorBinario).append(" ");
        }

        // Quitar el último espacio extra
        return binarios.toString().trim();
	}

	/**
	 * 
	 * @return
	 */
	private static String mensaje(){
		Scanner scan = new Scanner(System.in);
		System.out.println("Ingrese el texto: ");
		String text = scan.nextLine();
		return text;
	}

	/**
	 * 
	 * @param args
	 * @throws IOException
	 * @throws UnknownHostException
	 * @throws InterruptedException
	 */
	public static void main(String[] args) 
		throws IOException, UnknownHostException, InterruptedException{
		// String data = "1010101111001101"; // Example data
        // String data = "110010101111";
		String message = mensaje();
		String bin = string_to_bin(message);
		System.out.println(bin);
		String[] bins = bin.split(" ");
		StringBuilder transmisionBuilder = new StringBuilder();
		for (int i = 0; i < bins.length; i++){
			String text = calculateCRC(bins[i]);
			String concatenado = bins[i] + text;
			if (i > 0) {
				transmisionBuilder.append(" ");  // Agrega un espacio entre los valores
			}
			transmisionBuilder.append(concatenado);
		}
		String transmision = transmisionBuilder.toString();
        // String data = "100110111";
        // String crc = calculateCRC(data);
        // String transmittedData = data + crc;
        // System.out.println("CRC generated: " + crc);
        // System.out.println("Codeword transmitted: " + transmittedData);

		//ObjectOutputStream oos = null; //para serialized objects
		OutputStreamWriter writer = null;
		System.out.println("Emisor Java Sockets\n");

		//crear socket/conexion
		Socket socketCliente = new Socket(InetAddress.getByName(HOST), PORT);

		//mandar data 
		System.out.println("Enviando Data\n");
		//streamwriter para escribir data/bits/etc.
		writer = new OutputStreamWriter(socketCliente.getOutputStream());
		writer.write(transmision);	//enviar payload
		Thread.sleep(100);	//leve espera, opcional

		//limpieza
		System.out.println("Liberando Sockets\n");
		writer.close();
		socketCliente.close();
	}
}
