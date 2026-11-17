import socket
import time

import dgrama
import router

R2_AD = ("127.0.0.1", 8882)

emisor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)       


if __name__ == "__main__":

    print(f"Enviando paquete con direccion final 127.0.0.1:8883")
    emisor_socket.sendto(dgrama.Dgram.create_packet(
        {"ip": "127.0.0.1",
         "port": 8883,
         "msg": "mensaje para el tercer router"}), R2_AD)


    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        emisor_socket.close()

        



