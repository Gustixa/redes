class CRC32:
    def crc(self, dividend: str, divisor: str) -> str:
        shift = len(dividend) - len(divisor)

        while shift >= 0:
            dividend = bin(int(dividend, 2) ^ (int(divisor, 2) << shift))[2:]
            shift = len(dividend) - len(divisor)

        if len(dividend) < 16:
            dividend = dividend.zfill(16)

        # print("div" + dividend)
        return dividend

def main():
    data, checksum, syn, dividend, received_data = "", "", "", "", ""
    padding = 0

    polynomial = "100000100110000010001110110110111"  # De 32 bits

    # data = "1010101111001101" # Sin errores
    # data = "110010101111" # Con 1 error
    data = "100110111" # con 2 o mas errores

    # dividend = data
    dividend = data + "0" * (len(polynomial) - 1)
    # padding = len(polynomial) - 1
    # for _ in range(padding):
    #     dividend += "0"

    obj = CRC32()
    checksum = obj.crc(dividend, polynomial)
    data_with_checksum = data + checksum
    print("Sender checksum:", checksum)
    print("Codeword transmitida a través de la red:", data_with_checksum)

    received_data = input("Ingrese el código recibido: ").strip()
    syn = obj.crc(received_data, polynomial)

    if int(syn, 2) == 0:
        print("No hay error en la transmisión")
    else:
        print("Error en la transmisión")

if __name__ == "__main__":
    main()
