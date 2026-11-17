import socket

import dgrama 

class Router:

    def __init__(self, bind_ad: tuple[str, int], filename: str):
        print(f"##### INICIANDO ROUTER {filename} #####")
        print(f"Direccion de vinculacion: {bind_ad}\n")
        self.rt_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bind_ad : tuple[str, int] = bind_ad
        self.rt_table : list[str] = None

        self.rt_socket.bind(self.bind_ad)  #vincular a la direccion
        self.load_route_table(filename)    #inicializacion de la tabla de rutas


    def load_route_table(self, filename: str):
        with open(f"../rutas/rutas{filename}.txt") as file:
            tabla_rutas = file.read()
            self.rt_table = tabla_rutas.split("\n")


    @staticmethod
    def main(bind_ad: tuple[str, int], filename: str):
        router = Router(bind_ad, filename)

        while True:
            segment, desde = router.rt_socket.recvfrom(1024) 
            print(segment.decode())


if __name__ == "__main__":
    bind_ad_r = ("127.0.0.1", 5000)
    Router.main(bind_ad_r, "R1")


    





