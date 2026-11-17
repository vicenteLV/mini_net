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


    def send_packet(self, final_ad: tuple[str, int], msg: str, next_ad: tuple[str, int]):
        #armar diccionario
        dict_segmento = {
            "ip": final_ad[0],
            "port": final_ad[1],
            "msg": msg
        }
        packet_segmento = dgrama.Dgram.create_packet(dict_segmento)

        #enviar a la siguiente direccion
        self.rt_socket.sendto(packet_segmento, next_ad)


    def check_routes(self, routes_file_name: str, destination_address: str) -> tuple[str, int]:
        if self.rt_table == None:
            self.load_route_table(routes_file_name)

        for linea in self.rt_table:
            linea_split = linea.split(" ")
            ip_linea = linea_split[0].split("/")[0] #no tomamos en cuenta mascara
            #calzar ip
            if destination_address[0] == ip_linea:
                puerto_dest = destination_address[1]
                if puerto_dest >= linea_split[1] and puerto_dest >= linea_split[2]:
                    return (linea_split[3], int(linea_split[4]))

        return None


    @staticmethod
    def main(bind_ad: tuple[str, int], filename: str):
        router = Router(bind_ad, filename)

        while True:
            segment, desde = router.rt_socket.recvfrom(1024) 
            print(segment.decode())


if __name__ == "__main__":
    bind_ad_r = ("127.0.0.1", 5000)
    Router.main(bind_ad_r, "R1")


    





