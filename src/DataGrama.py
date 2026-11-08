class DataGrama:


    def __init__(self, cadena: bytes):
        """inicializa estructura con header en formato str.encoded() i.e. con ';' """
        cadena_str = cadena.decode('utf-8')
        cadena_split = cadena_str.split(";")

        #ip como str y cadena de 4 bytes 
        self.dest_ip = cadena_split[0]
        self.dest_ip_bytes = bytes([int(p) for p in self.dest_ip.split(".")]) 

        #puerto (int y bytes)  
        self.dest_port = int(cadena_split[1])
        self.dest_port_bytes = self.dest_port.to_bytes(2)

        #mensaje (str y bytes)
        self.msg = cadena_split[2]
        self.msg_bytes = cadena_split[2].encode()
        self.msg_len = len(self.msg_bytes).to_bytes(2)

        #header completo en bytes (4 bytes IP - 2 bytes Puerto - 2 bytes de largo - mensaje), sin ';'
        self.header = self.dest_ip_bytes + self.dest_port_bytes + self.msg_len + self.msg_bytes

        #header con ';'
        self.header_original = cadena


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
    address = ("127.0.0.1")
    puerto = 5000
    mensaje = "hola que tal"

    



        