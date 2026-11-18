import socket

"""
header :: 
    IP(4bytes);Puerto(2bytes);TTL(1byte);ID(1);Offset(2);Size(4);FLAG(1) -> 15 bytes + mensaje

estructura header_bytes-> diccionario con campos ip, puerto, msg
estructura header parseado -> {'ip': ... 
                                'port': ...
                                'ttl': ...
                                'id': ...
                                'offset': ...
                                'size': ... -> del mensaje
                                'flag': ... -> si hay mas mensaje
                                'msg': ...}"""


class Dgram:
    size_header = 15 #en bytes

    def __init__(self, segment: bytes):
        self.header : bytes = segment
        self.header_dict : dict = self.parse_packet(self.header)


    @staticmethod
    def parse_packet(IP_packet: bytes) -> dict:
        dicc = {}
        ip = IP_packet[:4]
        port = IP_packet[4:6]
        ttl = IP_packet[6]
        id = IP_packet[7]
        offset = IP_packet[8:10]
        size = IP_packet[10:14]
        flag = IP_packet[14]
        msg = IP_packet[15:]
        
        dicc["ip"] = f"{ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}"   #str 4B
        dicc["port"] = int.from_bytes(port)               #int 2B
        dicc["ttl"] = ttl                                 #int 1B
        dicc["id"] = id                                   #int 1B
        dicc["offset"] = int.from_bytes(offset)           #int 2B
        dicc["size"] = int.from_bytes(size)               #int 4B
        dicc["flag"] = flag                               #int 1B --> 15B de header IP
        dicc["msg"] = msg.decode()                        #str    --> size B

        return dicc


    @staticmethod
    def is_ip_valid(octetos: list[int]) -> None:
        o = 1
        for oct in octetos:
            if oct > 255 or oct < 0:
                raise ValueError(f"[ERROR] Término {o} de la IP no es válido")
            o += 1



    @staticmethod
    def create_packet(parsed_IP_packet: dict) -> bytes:
        ip_ints = [int(o) for o in parsed_IP_packet["ip"].split(".")]
        #validacion de octetos en ipv4
        try:
            Dgram.is_ip_valid(ip_ints)
        except ValueError:
            print("[ERROR] No se pudo crear segmento\n")


        port_bytes = parsed_IP_packet["port"].to_bytes(2)
        ttl_bytes = bytes([parsed_IP_packet["ttl"]])
        id_bytes = bytes([parsed_IP_packet["id"]])
        offset_bytes = parsed_IP_packet["offset"].to_bytes(2)
        size_bytes = parsed_IP_packet["size"].to_bytes(4)
        flag_bytes = bytes([parsed_IP_packet["flag"]])

        header_ip_bytes = bytes(ip_ints)+port_bytes+ttl_bytes+id_bytes+offset_bytes+size_bytes+flag_bytes

        msg_bytes = parsed_IP_packet["msg"].encode()


        return header_ip_bytes + msg_bytes




def print_fragment(frags: list[Dgram]):
        i = 1
        for frag in frags:
            print(f"FRAGMENTO {i}")
            print(f"IP: {frag.header_dict["ip"]}")
            print(f"Port: {frag.header_dict["port"]}")
            print(f"TTL: {frag.header_dict["ttl"]}")
            print(f"ID: {frag.header_dict["id"]}")
            print(f"Offset: {frag.header_dict["offset"]}")
            print(f"Size: {frag.header_dict["size"]}")
            print(f"Flag: {frag.header_dict["flag"]}\n")
    
            i += 1

if __name__ == "__main__":

    #mini test para el parse_packet
    ip_str = "127.0.0.1"
    port_int = 5000
    ttl = 10
    id = 33
    offset = 56
    flag = 0
    msg_str1 = "mensaje de prueba, necesita ser un poco mas largo para probar la fragmentacion"
    msg_str2 = "corto"
    size1 = len(msg_str1.encode())
    size2 = len(msg_str2.encode())

    ip_int = [int(p) for p in ip_str.split(".")]
    port_bytes = port_int.to_bytes(2)
    ttl_bytes = bytes([ttl])
    id_bytes = bytes([id])
    offset_bytes = offset.to_bytes(2)

    size1_bytes = size1.to_bytes(4)
    size2_bytes = size2.to_bytes(4)

    flag_bytes = bytes([flag])

    header_ip_bytes1 = bytes(ip_int)+port_bytes+ttl_bytes+id_bytes+offset_bytes+size1_bytes+flag_bytes 
    header_ip_bytes2 = bytes(ip_int)+port_bytes+ttl_bytes+id_bytes+offset_bytes+size2_bytes+flag_bytes 

    segment_bytes1 = header_ip_bytes1 + msg_str1.encode()
    segment_bytes2 = header_ip_bytes2 + msg_str2.encode()

    dgram1 = Dgram(segment_bytes1)
    dgram2 = Dgram(segment_bytes2)

    dict_test = dgram1.header_dict

    assert(dict_test["ip"] == ip_str)
    assert(dict_test["port"] == port_int)
    assert(dict_test["msg"] == msg_str1)
    assert(dict_test["ttl"] == ttl)
    assert(dict_test["id"] == id)
    assert(dict_test["offset"] == offset)
    assert(dict_test["size"] == size1)
    assert(dict_test["flag"] == flag)


    #corroborando que el segmento pasado por parse y create queda igual
    assert(segment_bytes1 == dgram1.create_packet(dict_test))

    print("##### PROBANDO FRAGMENTACION #####")
    fragmentos1 = fragment_IP_packet(segment_bytes1, 25)


    print_fragment(fragmentos1)

    print("--> Fragmentacion de mensaje corto")
    fragmentos2 = fragment_IP_packet(segment_bytes2, 25)
    print_fragment(fragmentos2)
    assert(len(fragmentos2) == 1)
    


    


