import socket
import DataGrama


class Router:
    #datagramas que va pasando
    on_queue: list[DataGrama.DataGrama] = []
    rt_table: list[str] = []

    def __init__(self, ad: str, port: int):
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bind_ad: tuple[str, int] = (ad, port) 

        #conexion y escuchar
        self.socket.bind(self.bind_ad)
        print(f"[OK] Socket escuchando en dirección {self.bind_ad}")


    def format_route_table(self, filename: str):
        ruta_tabla = f"../rutas/{filename}.txt"
        with open(ruta_tabla) as tabla:
            tabla_txt = tabla.read()

            self.rt_table = tabla_txt.split("\n")        




    def redirect(self, ip: str, port: int) -> tuple[str, int]:
        #reviso linea por linea
        for line in self.rt_table:
            fila = line.split(" ")
            ip_line = fila[0].split("/")[0] #por ahora sin mascara

            #calza ip
            if ip == ip_line:
                puerto_inicial = int(fila[1])
                puerto_final = int(fila[2])

                #calza puerto
                if port >= puerto_inicial and port <= puerto_final:
                    ip_hop = fila[3]
                    port_hop = int(fila[4])

                    return (ip_hop, port_hop) 
                else:
                    print("[DEBUG] puerto no calza, revisando siguiente linea")
            else:
                print("[DEBUG] IP no calza, revisando siguiente linea")

        print("[ERROR] No se encontro siguiente salto")






    def recv_header_ip(self, header_ip: bytes, emisor: tuple[str, int]):

        datagrama_recvd = DataGrama.DataGrama(header_ip)

        if datagrama_recvd.dest_ad == self.bind_ad[0] and datagrama_recvd.dest_port == self.bind_ad[1]:
            print(f"Mensaje: {datagrama_recvd.mensaje}\nDesde {emisor}")
        else:
            next_hop = self.redirect(datagrama_recvd.dest_ad, datagrama_recvd.dest_port)
            self.socket.sendto(header_ip, next_hop)

        


if __name__ == "__main__":
    puerto = int(input("Router número: "))
    R1 = Router("127.0.0.1", 8880 + puerto)

    while True:
        nombre_tabla = f"rutasR{puerto}"
        R1.format_route_table(nombre_tabla)
        mensaje, desde = R1.socket.recvfrom(1024)

        R1.recv_header_ip(mensaje, desde)

        

