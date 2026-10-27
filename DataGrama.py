class DataGrama:

    def __init__(self, ad: str, port: int, mensaje: str):
        self.dest_ad = ad
        self.dest_port = port
        self.mensaje = mensaje
        self.header_tcp: bytes= self.get_header_tcp()



    def get_header_tcp(self) -> bytes:
        """Datagrama -> bytes
        toma los atributos del DataGrama y los traduce 
        a un header tcp
        HEADER: 4 bytes IP - 2 bytes Puerto - 2 Bytes de largo - mensaje"""

        dest_ad_bytes = self.ip_to_bytes(self.dest_ad)
        dest_port_bytes = self.dest_port.to_bytes(2)

        #codificar mensaje
        msg_bytes = self.mensaje.encode()
        msg_len = len(msg_bytes).to_bytes(2)

        return dest_ad_bytes + dest_port_bytes + msg_len + msg_bytes


    @classmethod
    def get_info_header(self) -> tuple[str, int, str]:
        """DataGrama -> str int str
        toma un header tcp en bytes y saca la informacion"""

        ad_bytes = self.header_tcp[:4]
        ad_str = ".".join(str(b) for b in ad_bytes)

        port = int.from_bytes(2, self.header_tcp[4:6])
        msg_len = int.from_bytes(2, self.header_tcp[6:8])

        msg_bytes = self.header_tcp[8 : 8 + msg_len]
        msg = msg_bytes.decode('utf-8')

        return (ad_str, port, msg)



    @staticmethod
    def ip_to_bytes(id_ad: str) -> bytes:
        """str -> bytes
        convierde cualquier ipv4 en formato str a una lista bytes de
        largo 4"""
        chunks = [int(p) for p in id_ad.split(".")]

        return bytes([chunks])


    @staticmethod
    def valid_address(ad: str) -> bool:
        ad_split = ad.split(".")  #lista de enteros 
        if len(ad_split) != 4:
            print("[DEBUG] Direccion n tiene 4 int separados")
            return False

        for num in ad_split:
            if not num.isdigit():
                print("[DEBUG] num no es valido")
                return False
            
            num_int = int(num)
            #validacion del rango, si es un int mayor a 8 bits
            if num_int < 0 or num_int > 255:
                return False

        return True



if __name__ == "__main__":
    address = ("localhost")
    puerto = 5000
    mensaje = "hola que tal"

    d1 = DataGrama(address, puerto, mensaje)

    print(d1.header_tcp)



        