import java.util.Scanner;

public class App {
    public static void main(String[] args) throws Exception { 
        String data, checksum, syn, dividend, Received_data;
        int padding;

        // String polynomial = "1000100000010000"; // De 16 bits
        String polynomial = "100000100110000010001110110110111"; // De 32 bits

        Scanner sc = new Scanner(System.in);
        System.out.println("Ingrese la data para ser encriptada: ");
        data = sc.next();

        dividend = data;
        padding = polynomial.length() - 1;
        for(int i = 0; i < padding; i++){
            dividend += "0";
        }

        CRC32 obj = new CRC32();
        checksum = obj.CRC(dividend, polynomial);
        data += checksum;
        System.out.println("Sender checksum " + checksum);
        System.out.println("Codeword transmitida a traves de la red" + data);
        System.out.println("Ingrese el codigo recivido");
        Received_data = sc.next();
        syn = obj.CRC(Received_data, polynomial);

        if(Long.parseLong(syn) == 0){
            System.out.println("No hay error en la transmision");
        } else {
            System.out.println("Error en la transmision");
        }
    
    }
}
