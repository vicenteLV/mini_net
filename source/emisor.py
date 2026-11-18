import socket
import time

import dgrama
import router

NUMBER_OF_ROUTERS = 3
R1_AD = ("127.0.0.1", 8881)

emisor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)        


if __name__ == "__main__":
    paquete = dgrama.Dgram.create_packet({
        "ip": "127.0.0.1",
        "port": 8883,
        "ttl": 10,
        "id": 30,
        "offset": 30,
        "size": 400,
        "flag": 0,
        "msg": "mensaje de prueba para check"            
        })


    emisor_socket.sendto(paquete, R1_AD)


    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        emisor_socket.close()

        



