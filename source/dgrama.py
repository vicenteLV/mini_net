import socket

"""
header :: IP(4bytes);Puerto(2bytes);mensaje
estructura header_bytes-> diccionario con campos ip, puerto, msg
estructura header parseado -> {'ip': ... 
                                'port': ...
                                'msg': ...}"""


class Dgram:

    def __init__(self, segment: bytes):
        self.header : bytes = segment
        self.header_dict : dict = {}


    def parse_packet(self, IP_packet: bytes) -> dict:
        dicc = {}
        ip = IP_packet[:4]
        port = IP_packet[4:6]
        msg = IP_packet[6:]
        
        dicc["ip"] = f"{ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}"
        dicc["port"] = int.from_bytes(port)
        dicc["msg"] = msg.decode()

        return dicc


    @staticmethod
    def is_ip_valid(octetos: list[int]) -> None:
        o = 1
        for oct in octetos:
            if oct > 255 or oct < 0:
                raise ValueError(f"[ERROR] Término {o} de la IP no es válido")
            o += 1



    def create_packet(self, parsed_IP_packet: dict) -> bytes:
        ip_ints = [int(o) for o in parsed_IP_packet["ip"].split(".")]
        #validacion de octetos en ipv4
        try:
            self.is_ip_valid(ip_ints)
        except ValueError:
            print("[ERROR] No se pudo crear segmento\n")


        port_bytes = parsed_IP_packet["port"].to_bytes(2)
        msg_bytes = parsed_IP_packet["msg"].encode()

        return bytes(ip_ints) + port_bytes + msg_bytes



if __name__ == "__main__":

    #mini test para el parse_packet
    ip_str = "127.0.0.1"
    port_int = 5000
    msg_str = "mensaje de prueba"

    ip_int = [int(p) for p in ip_str.split(".")]
    port_bytes = port_int.to_bytes(2)

    segment_bytes = bytes(ip_int) + port_bytes + msg_str.encode()
    dgram = Dgram(segment_bytes)

    dict_test = dgram.parse_packet(segment_bytes)

    assert(dict_test["ip"] == ip_str)
    assert(dict_test["port"] == port_int)
    assert(dict_test["msg"] == msg_str)

    #corroborando que el segmento pasado por parse y create queda igual
    assert(segment_bytes == dgram.create_packet(dict_test))

    


