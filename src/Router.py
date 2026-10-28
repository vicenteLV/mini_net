import socket
import DataGrama


class Router:
    #datagramas que va pasando
    on_queue: list[DataGrama.DataGrama] = []
    rt_table: str = ""

    def __init__(self, ad: str, port: int):
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bind_ad: tuple[str, int] = (ad, port) 

        #conexion y escuchar
        self.socket.bind(self.bind_ad)
        print(f"[OK] Socket escuchando en dirección {self.bind_ad}")


    def format_route_table(self, filename: str):
        ruta_tabla = f"../routes/{filename}.txt"
        with open(ruta_tabla) as tabla:
            self.rt_table = tabla.read()        




    def recv_header_ip(self, header_ip: bytes, emisor: tuple[str, int]):

        datagrama_recvd = DataGrama.DataGrama(header_ip)

        if datagrama_recvd.dest_ad == self.bind_ad[0] and datagrama_recvd.dest_port == self.bind_ad[1]:
            print(f"Mensaje: {datagrama_recvd.mensaje}\nDesde {emisor}")
        else:
            print(f"[DEBUG] Redireccionando hacia ({datagrama_recvd.dest_ad}, {datagrama_recvd.dest_port})")

        








if __name__ == "__main__":
    R1 = Router("127.0.0.1", 5000)

    while True:
        mensaje, desde = R1.socket.recvfrom(1024)

        R1.recv_header_ip(mensaje, desde)

        

