UNIVERSIDAD DEL VALLE DE GUATEMALA

Facultad de Ingeniería

CC3085 – Redes

Sección 10

Ing. Miguel Novella Linare

Laboratorio 2

Samuel Argueta - 211024

Alejandro Martinez - 21430

GUATEMALA, 25 de julio de 2024


[Log](./Log.html)

[Stats](./Stats.html)

# DESCRIPCIÓN DE LA PRÁCTICA
En este caso, el propósito del laboratorio es familiarizarse con el concepto de capas de una manera práctica enviando mensajes de manera local entre un “emisor” y un “receptor” emulado de manera local, en donde, los mensajes deberán ser traducidos a binario y, en algunos casos, poseer errores, justo como sucedería en un escenario real. Se debe solicitar un mensaje de entrada, que es lo que el Emisor desea transmitir, el cual deberá ser traducido a binario. El Receptor recibirá este código binario y deberá validar que esté bien, en caso de estarlo, mostrará el mensaje, en caso contrario, mostrará mensaje de error.
# METODOLOGÍA
Utilización del concepto de Sockets para la comunicación entre clientes, esto con el fin de poder enviar y recibir mensajes de manera simulada entre emisor y receptor. En donde cada uno tendrá su implementación en lenguajes diferentes, con el fin de poder ser más realista la simulación. En este caso se tiene registro de cada uno de los envíos que se realizan del emisor a receptor mediante un archivo .log para constatar cada uno de los resultados.
# RESULTADOS
Graficas, capturas, etc.
# DISCUSIÓN
CRC32 es altamente fiable para la detección de errores en los datos transmitidos, pero carece en la corrección de los mismos. Este no corrige los errores, pero es extremadamente eficaz para detectarlos. Su poder está en que puede detectar rafagas de errores, esto se entiende por varios bits incorrectos en la transmisión pero, si la tasa de errores es alta, lo detecta, solo que se debe realizar una retransmisión de datos o el uso de un algoritmo adicional.

En contraparte, Hamming no solo detecta errores, sino que también los corrige. Este es mas flexible para manejar y corregir errores de 1 solo bit, pero su capacidad de corrección disminuye drásticamente cuando aumenta la tasa de errores. No puede corregir errores en rafaga, es decir, múltiples bits con problemas en la transmisión.

Cada uno tiene su escenario de uso. Hamming es útil en situaciones donde la corrección de errores es crucial; CRC32 es eficiente y rápido en la detección de errores, lo que lo hace adecuado para entornos donde la corrección de errores no es crítica, pero la detección rápida es esencial.

| Algoritmos de detección de errores (CRC32) | Algoritmos de Corrección de errores (Hamming Code)|
|--|--|
| Alta tasa de errores, esto es cuando la probabilidad de errores es alta y la corrección en el lugar no es factible o eficiente. | Baja tasa de errores, donde los errores son raros y se pueden manejar de manera eficiente en el lugar. |
| Retransmisión de datos, donde es viable transmitir datos, como en redes de computadoras, se puede utilizar para detectar errores y solicitar una retransmisión si se detecta un error. | Crítica de corrección en tiempo real, aplicaciones críticas donde la corrección en tiempo real es esencial, como en sistemas de memoria de computadoras y comunicaciones espaciales. |
| Simplicidad y eficiencia, cuando se necesita un método simple y eficiente para verificar la integridad de los datos sin la sobrecarga de la corrección de errores. | Limitación de retransmisión, Cuando la retransmisión de datos no es posible o deseable debido a restricciones de tiempo o ancho de banda. |


# CONCLUSIONES
Cada algoritmo es útil según las necesidades. CRC32 es más adecuado para la detección rápida y eficiente de errores en sistemas donde la retransmisión es una opción. Hamming Code es ideal para entornos donde la corrección de errores en tiempo real es crucial y la tasa de errores es baja.
REFERENCIAS
Ritter, C. (2016, March 6). A painless guide to CRC error detection algorithms. Command Line Fanatic. https://commandlinefanatic.com/cgi-bin/showarticle.cgi?article=art008
GeeksforGeeks. (n.d.). Modulo-2 binary division. Retrieved August 1, 2024, from https://www.geeksforgeeks.org/modulo-2-binary-division/
GeeksforGeeks. (n.d.). Hamming code in computer network. Retrieved August 1, 2024, from https://www.geeksforgeeks.org/hamming-code-in-computer-network/
TechTarget. (n.d.). Hamming code. Retrieved August 1, 2024, from https://www.techtarget.com/whatis/definition/Hamming-code


