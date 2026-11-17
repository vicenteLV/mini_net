import socket

import dgrama 

class Router:

    def __init__(self, bind_ad: tuple[str, int], filename: str):
        print(f"##### INICIANDO ROUTER {filename} #####")
        print(f"Direccion de vinculacion: {bind_ad}")
        self.name = filename
        self.rt_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bind_ad : tuple[str, int] = bind_ad
        self.rt_table : list[str] = None

        self.rt_socket.bind(self.bind_ad)  #vincular a la direccion
        self.load_route_table(filename)    #inicializacion de la tabla de rutas

        self.print_table()


    def print_table(self):
        print("+-------------------------------------+")
        print(f"|        TABLA DE RUTAS DE {self.name}         |")
        print("+-------------------------------------+")
        for linea in self.rt_table:
            print(f"|{linea}|")
        print("+-------------------------------------+\n")


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


    def check_routes(self, destination_address: tuple[str, int]) -> tuple[str, int]:

        for linea in self.rt_table:
            linea_split = linea.split(" ")
            ip_linea = linea_split[0].split("/")[0] #no tomamos en cuenta mascara
            #calzar ip
            if destination_address[0] == ip_linea:
                puerto_dest = destination_address[1]
                if puerto_dest >= int(linea_split[1]) and puerto_dest <= int(linea_split[2]):
                    return (linea_split[3], int(linea_split[4]))

        return None

    def recv_segment(self):
        segment, desde = self.rt_socket.recvfrom(1024) 
        print(f"###### {self.name} ######")
        segment_dgram = dgrama.Dgram(segment) #con esto ya tenemos header(segmento) y diccionario del mensaje
        segment_dest = (segment_dgram.header_dict["ip"], segment_dgram.header_dict["port"])

        #si es el router de destino
        if segment_dest[0] == self.bind_ad[0] and segment_dest[1] == self.bind_ad[1]:
            print(f"Mensaje recibido desde {desde}:")
            print(f"{segment_dgram.header_dict["msg"]}\n")

        else: 
            next_hop = self.check_routes(segment_dest)
            if next_hop == None:
                print(f"[ERROR] No hay rutas hacia {segment_dest} => DESCARTADO\n")
            else:
                print(f"[INFO] Redirigiendo paquete con destino final {segment_dest} desde {self.bind_ad} hacia {next_hop}\n")
                self.send_packet(segment_dest, segment_dgram.header_dict["msg"], next_hop)


    @staticmethod
    def main(bind_ad: tuple[str, int], filename: str):
        router = Router(bind_ad, filename)

        #ciclo de recepcion de mensajes
        while True:
            router.recv_segment()



if __name__ == "__main__":
    bind_ad_r = ("127.0.0.1", 5000)
    Router.main(bind_ad_r, "R1")


    





