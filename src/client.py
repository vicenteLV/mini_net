import socket
import time

import DataGrama

#lista de paquetes para testear el forwarding
paquetes = [
    {"ip": "127.0.0.1", "port": 8881, "msg": "mensaje para el primer router"},
    {"ip": "127.0.0.1", "port": 8882, "msg": "mensaje para el segundo router"},
    {"ip": "127.0.0.1", "port": 8883, "msg": "mensaje para el tercer router"},
    {"ip": "127.0.0.1", "port": 8884, "msg": "mensaje para el cuarto router"}
]

def send_package(package_dict: dict, client_socket: socket.socket, 
                 ad: tuple[str, int]):
    
    header = DataGrama.DataGrama.create_packet(package_dict)

    print(f"Enviando paquete a {(package_dict["ip"], package_dict["port"])}")
    client_socket.sendto(header, ad)



if __name__ == "__main__":
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for pack in paquetes:
        for i in range(1,4):
            address = ("127.0.0.1", 8880 + i)
            print(f"Destino final: {(pack["ip"], pack["port"])}\n")
            send_package(pack, cliente_socket, address)
            time.sleep(3)

    



        


