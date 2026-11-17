import socket
import time

import dgrama
import router

NUMBER_OF_ROUTERS = 3

emisor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

paquetes = [
    {"ip": "127.0.0.1", "port": 8881, "msg": "mensaje para el router 1"},
    {"ip": "127.0.0.1", "port": 8882, "msg": "mensaje para el router 2"},
    {"ip": "127.0.0.1", "port": 8883, "msg": "mensaje para el router 3"},
    {"ip": "127.0.0.1", "port": 8890, "msg": "mensaje para el router 4"},
]


if __name__ == "__main__":
    #TEST para parte 6
    for pack in paquetes:
        segmento_pack = dgrama.Dgram.create_packet(pack)

        for i in range(1, NUMBER_OF_ROUTERS + 1):
            """
            se prueba envío a cada router y se analiza en la salida de main.py
            por donde se mueven los segmentos,
            al enviar segmentos, se comprueba en la consola de main.py que recorren segun las rutas
            definidas en sus tablas, y que el segmento a 127.0.0.1:8890 se descarta al no haber 
            destino con ese puerto
            """
            emisor_socket.sendto(segmento_pack, ("127.0.0.1", 8880 + i))
            time.sleep(1)

        



