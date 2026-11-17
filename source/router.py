import socket

import dgrama 

DEFAULT_AD = ("127.0.0.1", 7000) #direccion del router default

class Router:

    def __init__(self, bind_ad: tuple[str, int], filename: str, default: bool = False):
        print(f"##### INICIANDO ROUTER {filename} #####")
        print(f"Direccion de vinculacion: {bind_ad}")
        self.name: str = filename
        self.rt_socket:socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bind_ad: tuple[str, int] = bind_ad
        self.rt_table: list[str] = None
        self.DEFAULT: bool = default

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


    def rt_table_to_txt(self) -> str:
        txt = ""
        for linea in self.rt_table:
            txt += linea

        return txt


    def check_routes(self, destination_address: tuple[str, int], debug = False) -> tuple[str, int]:

        for linea in self.rt_table:
            linea_split = linea.split(" ")
            ip_linea = linea_split[0].split("/")[0] #no tomamos en cuenta mascara
            #calzar ip
            if destination_address[0] == ip_linea:
                puerto_dest = destination_address[1]
                if puerto_dest >= int(linea_split[1]) and puerto_dest <= int(linea_split[2]):

                    #round-robin
                    self.rt_table.remove(linea)
                    self.rt_table.append(linea)
                    if debug:
                        print(f"[DEBUG] Nueva tabla de rutas para {self.name}")
                        self.print_table()

                    return (linea_split[3], int(linea_split[4]))

        return None

    def recv_segment(self):
        segment, desde = self.rt_socket.recvfrom(1024) 
        print(f"###### {self.name} ######")
        segment_dgram = dgrama.Dgram(segment) #con esto ya tenemos header(segmento) y diccionario del mensaje, sirve para tomar desiciones
        segment_dest = (segment_dgram.header_dict["ip"], segment_dgram.header_dict["port"])
             
        #si es el router de destino o por defecto
        if segment_dest[0] == self.bind_ad[0] and segment_dest[1] == self.bind_ad[1]:
            print(f"Mensaje recibido desde {desde}:")
            print(f"{segment_dgram.header_dict["msg"]}\n")

        else: 
            next_hop = self.check_routes(segment_dest, True)
            if next_hop == None:
                if not self.DEFAULT:
                    #redirecciona a router default
                    print(f"[ERROR] No hay rutas hacia {segment_dest} => ENVIADO A ROUTER DEFAULT\n")
                    self.rt_socket.sendto(segment, DEFAULT_AD)

                else:
                    #imprime mensaje sin lugar en la red
                    print(f"Mensaje recibido desde {desde}:")
                    print(f"{segment_dgram.header_dict["msg"]}\n")
                    
            else:
                print(f"[INFO] Redirigiendo paquete con destino final {segment_dest} desde {self.bind_ad} hacia {next_hop}\n")
                self.rt_socket.sendto(segment, next_hop)


    @staticmethod
    def main(bind_ad: tuple[str, int], filename: str, default: bool = False):
        if default:
            router = Router(bind_ad, filename, True)
        else:
            router = Router(bind_ad, filename)

        #ciclo de recepcion de mensajes
        while True:
            router.recv_segment()



if __name__ == "__main__":
    bind_ad_r = ("127.0.0.1", 5000)
    Router.main(bind_ad_r, "R1")


    





