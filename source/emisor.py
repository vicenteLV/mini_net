import socket
import time

import dgrama
import router

NUMBER_OF_ROUTERS = 3
R1_AD = ("127.0.0.1", 8881)

emisor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

paquetes = [
    {"ip": "127.0.0.1", "port": 8881, "msg": "mensaje para el router 1"},
    {"ip": "127.0.0.1", "port": 8882, "msg": "mensaje para el router 2"},
    {"ip": "127.0.0.1", "port": 8883, "msg": "mensaje para el router 3"},
    {"ip": "127.0.0.1", "port": 8884, "msg": "mensaje para el router 4"},
    {"ip": "127.0.0.1", "port": 8885, "msg": "mensaje para el router 5"},
    {"ip": "127.0.0.1", "port": 8890, "msg": "mensaje para el router 10"},
]



def test_pack_sending(n: int) -> bool:
    """
    TEST para parte 6/8

    se prueba envío de paquetes con destinos finales distintos y se revisa en la salida
    de consola de main.py que sigan las rutas definidas por las tablas; se definen las pruebas
    segun router:
    -> Mensaje a R1 se envía a: 8881, 8883, 8883,
    -> Mensaje a R2 se envía a: 8882, 8885, 8885
    -> Mensaje a R3 se envía a: 8883, 8884, 8884 -> se repite 8884 para comprobar round robin
    -> Mensaje a R4 se envía a: 8884, 8881, 8881
    -> Mensaje a R5 se envía a: 8885, 8881, 8881 -> se repite 8884 para comprobar round robin
    -> Mensaje a R10 (no existe) se envía a: 8881, 8885 -> comprobar que paquete se descarta siempre
    """

    destinos = [[8881, 8883, 8883],       #destino final 8881
                [8882, 8885, 8885],       #destino final 8882
                [8883, 8884, 8884],       #destino final 8883
                [8884, 8881, 8881],       #destino final 8884
                [8885, 8881, 8881],       #destino final 8885
                [8881, 8885]              #destino final 8890
                ]
    pack = paquetes[n]
    segmento_pack = dgrama.Dgram.create_packet(pack)

    for dest in destinos[n]:
        print(f"[INFO] Enviando paquete a {pack["ip"]}:{pack["port"]} por 127.0.0.1:{dest}")
        emisor_socket.sendto(segmento_pack, ("127.0.0.1", dest))
        time.sleep(1)


def test_send_default():
    #para solo un caso
    
    segmento_pack = dgrama.Dgram.create_packet({
        "ip": "128.0.0.1",
        "port": 8900,
        "msg": "Mensaje para el router default"
    })

    #prueba desde el R1 al R5
    for i in range(1, 6):
        print(f"[INFO] Enviando paquete fuera de la red, siguiente salto 127.0.0.1:888{i}")
        emisor_socket.sendto(segmento_pack, ("127.0.0.1", 8880 + i))
        time.sleep(1)


        


if __name__ == "__main__":

    """
    print("##### VIENDO ENVÍOS DE PAQUETES #####")
    for i in range(len(paquetes)):
        test_pack_sending(i)
        time.sleep(2)


    print("##### ENVÍO FUERA DE LA RED #####")
    test_send_default()
    """

    pack = dgrama.Dgram.create_packet({
        "ip": "127.0.0.1",
        "port": 8885,
        "msg": "mensaje para el router 5"
    })
    for i in range(3):
        print(f"Enviando paquete para R5 a traves de R1")
        emisor_socket.sendto(pack, R1_AD)
        time.sleep(5)


    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        emisor_socket.close()

        



