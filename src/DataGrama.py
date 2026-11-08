class DataGrama:


    def __init__(self, cadena: bytes):
        """inicializa estructura con header en formato str.encoded() i.e. con ';' """
        cadena_str = cadena.decode('utf-8')
        cadena_split = cadena_str.split(";")

        #ip como str y cadena de 4 bytes 
        self.dest_ip = cadena_split[0]        
        self.dest_ip_bytes = self.ip_to_bytes(self.dest_ip) 


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



    def parse_packet(IP_packet: bytes):
        """bytes -> dict
        recibe paquete en el formato sin ';' y lo pasa a un diccionario"""
        packet_dict = {}

        #IP
        ip_octs= []
        for i in range(4):
            ip_digit = IP_packet[i]
            ip_octs.append(ip_digit)

        packet_dict["ip"] = f"{ip_octs[0]}.{ip_octs[1]}.{ip_octs[2]}.{ip_octs[3]}"

        #puerto
        puerto_bytes = IP_packet[4:6]
        packet_dict["port"] = int.from_bytes(puerto_bytes, byteorder='big')

        #mensaje
        packet_dict["msg"] = IP_packet[6:].decode('utf-8')

        return packet_dict





    @staticmethod
    def ip_to_bytes(id_ad: str) -> bytes:
        """str -> bytes
        convierde cualquier ipv4 en formato str a una lista bytes de
        largo 4"""
        #corroborar que sea una IPv4 valida
        partes_ip = id_ad(".")
        if len(partes_ip) != 4:
            raise ValueError("Una IPv4 debe tener exactamente 4 octetos")

        for octeto in partes_ip:
            if int(octeto) > 255 or int(octeto) < 0:
                raise ValueError(f"Valores de IP deben estar entre 0 y 255")

        
        return bytes([int(p) for p in partes_ip]) 



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

    



        