class DataGrama:


    def __init__(self, cadena: bytes):
        """inicializa estructura con header en formato str.encoded()"""
        cadena_str = cadena.decode('utf-8')
        cadena_split = cadena_str.split(";")

        self.dest_ad = cadena_split[0]
        self.dest_port = int(cadena_split[1])
        self.mensaje = cadena_split[2]



    def get_header_ip(self) -> bytes:
        """Datagrama -> bytes
        toma los atributos del DataGrama y los traduce 
        a un header ip
        HEADER: 4 bytes IP - 2 bytes Puerto - 2 Bytes de largo - mensaje"""

        dest_ad_bytes = self.ip_to_bytes(self.dest_ad) #4 bytes
        dest_port_bytes = self.dest_port.to_bytes(2)   #2 bytes

        #codificar mensaje
        msg_bytes = self.mensaje.encode()
        msg_len = len(msg_bytes).to_bytes(2)           #2 bytes

        return dest_ad_bytes + dest_port_bytes + msg_len + msg_bytes




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

    print(d1.header_ip)



        