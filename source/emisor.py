import socket
import time

import dgrama
import router

NUMBER_OF_ROUTERS = 3
R1_AD = ("127.0.0.1", 8881)

emisor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)        


if __name__ == "__main__":

    


    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        emisor_socket.close()

        



