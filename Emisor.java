//Sockets en Java - Emisor
//Miguel Novella - Redes UVG - 2023

//Para TCP usar Socket, para UDP DatagramSocket
//En versiones anteriores de java todo era via Socket(stream/datagram)
//para recibir se usar ServerSocket
import java.net.Socket;
import java.net.InetAddress;
//input stream reader para leer
import java.io.OutputStreamWriter;

import java.io.IOException;		//exceptions
import java.net.UnknownHostException;

public class Emisor{

	private static String	HOST = "127.0.0.1";	//a.k.a. localhost, o loopback
	private static int	PORT = 65432;		//elegir puerto
	private static String 	payload = "Hola Mundo Java 11";		//payload a enviar
	
	public static void main(String[] args) 
		throws IOException, UnknownHostException, InterruptedException{

		//ObjectOutputStream oos = null; //para serialized objects
		OutputStreamWriter writer = null;
		System.out.println("Emisor Java Sockets\n");

		//crear socket/conexion
		Socket socketCliente = new Socket(InetAddress.getByName(HOST), PORT);

		//mandar data 
		System.out.println("Enviando Data\n");
		//streamwriter para escribir data/bits/etc.
		writer = new OutputStreamWriter(socketCliente.getOutputStream());
		writer.write(payload);	//enviar payload
		Thread.sleep(100);	//leve espera, opcional

		//limpieza
		System.out.println("Liberando Sockets\n");
		writer.close();
		socketCliente.close();

		//TODO escuchar response		
	}
}
