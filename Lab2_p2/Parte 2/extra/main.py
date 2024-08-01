def texto_a_binario(texto):
    # Inicializar una lista para almacenar los valores binarios
    binarios = []
    
    # Iterar sobre cada carácter en el texto
    for char in texto:
        # Obtener el valor ASCII del carácter
        valor_ascii = ord(char)
        
        # Convertir el valor ASCII a binario y asegurar que tenga 8 bits
        valor_binario = format(valor_ascii, '08b')
        
        # Añadir el valor binario a la lista
        binarios.append(valor_binario)
    
    # Unir todos los valores binarios en una sola cadena separada por espacios
    
    return binarios

# Ejemplo de uso
texto = "Hola amigo!"
binario = texto_a_binario(texto)
print(binario)
