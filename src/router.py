#ejecucion: python3 router.py 127.0.0.1 8881 rutas.txt

import socket
import DataGrama
import sys


class Router:
    #datagramas que va pasando
    on_queue: list[DataGrama.DataGrama] = []
    rt_table: list[str] = []  #se descompone el contenido del txt correspondiente al router

    def __init__(self, ad: str, port: int):
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bind_ad: tuple[str, int] = (ad, port) 

        #conexion y escuchar
        self.socket.bind(self.bind_ad)
        print(f"[OK] Socket escuchando en dirección {self.bind_ad}\n")



    def check_routes(self, routes_file_name: str, destination_address: tuple[str, int]) -> tuple[str, int]:
        #guardar tabla correspondiente al router
        ruta_tabla = f"../rutas/{routes_file_name}"
        with open(ruta_tabla) as rt:
            tabla_txt = rt.read()
            self.rt_table = tabla_txt.split("\n")

        #reviso linea por linea
        for line in self.rt_table:
            fila = line.split(" ")
            ip_line = fila[0].split("/")[0] #por ahora sin mascara

            #calza ip
            if destination_address[0] == ip_line:
                puerto_inicial = int(fila[1])
                puerto_final = int(fila[2])

                #calza puerto
                if destination_address[1] >= puerto_inicial and destination_address[1] <= puerto_final:
                    ip_hop = fila[3]
                    port_hop = int(fila[4])

                    return (ip_hop, port_hop) 
                else:
                    print("[DEBUG] puerto no calza, revisando siguiente linea")
            else:
                print("[DEBUG] IP no calza, revisando siguiente linea")

        print("[ERROR] No se encontro PATH para paquete => DESCARTADO")
        return None




    def recv_header_ip(self, rt_filename: str, header_ip: bytes, emisor: tuple[str, int]):
        #para distinguir en prints
        nombre_router = rt_filename.split(".")[0][5:]

        dgram_recvd = DataGrama.DataGrama(header_ip) 

        print(f"\n####### {nombre_router} #######")

        if dgram_recvd.header_dict["ip"] == self.bind_ad[0] and dgram_recvd.header_dict["port"] == self.bind_ad[1]:
            print(f"Mensaje: {dgram_recvd.header_dict["msg"]}")
            print(f"Desde {emisor}\n")
        else:

            next_hop = self.check_routes(rt_filename, (dgram_recvd.header_dict["ip"], dgram_recvd.header_dict["port"]))
            if next_hop != None:    
                print(f"Redireccionando a {next_hop}")
                self.socket.sendto(header_ip, next_hop)
            else:
                print(f"[DEBUG] Paquete descartado")



    @staticmethod
    def main(ip_str, port, rt_table):
    
        R1 = Router(ip_str, int(port))
    
        while True:
            mensaje, desde = R1.socket.recvfrom(1024)
    
            R1.recv_header_ip(rt_table, mensaje, desde)

        


if __name__ == "__main__":
    Router.main(sys.argv[1], sys.argv[2], sys.argv[3])

        

