class CRC32:
    POLYNOMIAL = "100000100110000010001110110110111"

    @staticmethod
    def calculate_crc(data: str) -> str:
        dividend = data + "0" * 32
        dividend_int = int(dividend, 2)
        divisor_int = int(CRC32.POLYNOMIAL, 2)
        shift = len(dividend) - len(CRC32.POLYNOMIAL)

        while shift >= 0:
            dividend_int ^= divisor_int << shift
            shift = dividend_int.bit_length() - divisor_int.bit_length()

        crc = bin(dividend_int)[2:]  # Convertir a binario y eliminar el prefijo '0b'
        return crc.zfill(32)  # Padding a 32 bits

def main():
    # data = "1010101111001101"  # Datos de ejemplo
    # data = "110010101111"  # Datos de ejemplo
    data = "100110111"  # Datos de ejemplo con errores
    crc = CRC32.calculate_crc(data)
    transmitted_data = data + crc
    print("CRC generated:", crc)
    print("Codeword transmitted:", transmitted_data)
    
    received_data = input("Ingrese el código recibido: ").strip()
    syn = obj.crc(received_data, polynomial)

    if int(syn, 2) == 0:
        print("No hay error en la transmisión")
    else:
        print("Error en la transmisión")

if __name__ == "__main__":
    main()
