import socket
import DataGrama


class Router:
    #datagramas que va pasando
    on_queue: list[DataGrama.DataGrama] = []

    def __init__(self, ad: str, port: int):
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bind_ad: tuple[str, int] = (ad, port) 

        #conexion y escuchar
        self.socket.bind(self.bind_ad)
        print(f"[OK] Socket escuchando en dirección {self.bind_ad}")





if __name__ == "__main__":
    R1 = Router("127.0.0.1", 5000)

    while True:
        mensaje, desde = R1.socket.recvfrom(1024)
        d1 = DataGrama.DataGrama(mensaje)

        print(f"Mensaje: {d1.mensaje}\nDesde: {desde}")

        

