import socket
import time

import dgrama
import router

R1_AD = ("127.0.0.1", 8881)

emisor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        


if __name__ == "__main__":

    for i in range(3):
        pack = dgrama.Dgram.create_packet({
            "ip": "127.0.0.1",
            "port": 8885,
            "msg": "mensaje para el quinto router"
        })

        emisor_socket.sendto(pack, R1_AD)
        time.sleep(1)


    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        emisor_socket.close()

        



