import socket
import time

import DataGrama

#lista de paquetes para testear el forwarding
paquetes = [
    {"ip": "127.0.0.1", "port": 8881, "msg": "mensaje para el primer router"},
    {"ip": "127.0.0.1", "port": 8882, "msg": "mensaje para el segundo router"},
    {"ip": "127.0.0.1", "port": 8883, "msg": "mensaje para el tercer router"},
    {"ip": "127.0.0.1", "port": 8889, "msg": "mensaje para el noveno router"},
]

multiple_routes = [
    {"ip": "127.0.0.1", "port": 8885, "msg": "mensaje para R5 multiples rutas"}
]

def send_package(package_dict: dict, client_socket: socket.socket, 
                 ad: tuple[str, int]):
    
    header = DataGrama.DataGrama.create_packet(package_dict)

    print(f"Enviando paquete a: {ad[0]}:{ad[1]}")
    print(f"Destino final: {(package_dict["ip"], package_dict["port"])}\n")
    client_socket.sendto(header, ad)



if __name__ == "__main__":
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #envío de paquetes que deberían llegar
    for pack in paquetes:
        for i in range(1,4):
            address = ("127.0.0.1", 8880 + i)
            send_package(pack, cliente_socket, address)
            time.sleep(3)

    #envio de paquetes que deberían ser descartados
    for pack_mult in multiple_routes:
        if pack_mult["port"] == 8885:
            for i in range(3):
                #paquete enviado al R2 y se evalua si sigue distintas rutas
                rt_ad = ("127.0.0.1", 8882)
                send_package(pack_mult, cliente_socket, rt_ad)


    



        


