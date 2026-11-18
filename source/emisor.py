import socket
import time

import dgrama
import router

NUMBER_OF_ROUTERS = 3
R1_AD = ("127.0.0.1", 8881)

emisor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)        


if __name__ == "__main__":

    """
    """
    print("#####ENVIO ENTRE ROUTERS R1 y R3 para probar funcion check")
    mensaje = "mensaje de prueba para check, largo para ver si aguanta varios offset"
    paquete = dgrama.Dgram.create_packet({
        "ip": "127.0.0.1",
        "port": 8883,
        "ttl": 10,
        "id": 30,
        "offset": 0,
        "size": len(mensaje.encode()),
        "flag": 0,
        "msg": mensaje            
        })


    emisor_socket.sendto(paquete, R1_AD)




    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        emisor_socket.close()

        



