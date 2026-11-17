import socket

import dgrama
import router

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

paquetes = [
    {"dest_ip": "127.0.0.1", "dest_port": 8881, "msg": "mensaje para router 1",
     "next_ip": "127.0.0.1"}
]

