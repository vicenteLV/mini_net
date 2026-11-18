import socket
import time

import dgrama 

DEFAULT_AD = ("127.0.0.1", 7000) #direccion del router default

class Router:

    def __init__(self, bind_ad: tuple[str, int], filename: str):
        print(f"##### INICIANDO ROUTER {filename} #####")
        print(f"Direccion de vinculacion: {bind_ad}")
        self.name: str = filename
        self.rt_socket:socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bind_ad: tuple[str, int] = bind_ad
        self.rt_table: list[str] = None

        self.rt_socket.bind(self.bind_ad)  #vincular a la direccion
        self.load_route_table(filename)    #inicializacion de la tabla de rutas

        self.print_table()
        


    def print_table(self):
        print(f"------------TABLA DE RUTAS DE {self.name}-----------")
        print("-------------------------------------------")
        for linea in self.rt_table:
            print(f"{linea}")
        print("-------------------------------------------\n")


    def load_route_table(self, filename: str):
        with open(f"../rutas/rutas{filename}.txt") as file:
            tabla_rutas = file.read()
            self.rt_table = tabla_rutas.split("\n")


    def rt_table_to_txt(self) -> str:
        txt = ""
        for linea in self.rt_table:
            txt += linea

        return txt


    def send_pack(self, segmento: dgrama.Dgram, to: tuple[str, int]):
        diccionario = segmento.header_dict
        diccionario["ttl"] -= 1

        nuevo_pack = dgrama.Dgram.create_packet(diccionario)

        self.rt_socket.sendto(nuevo_pack, to)


    @staticmethod
    def insertion_sort_fragments(frags: list[dgrama.Dgram], campo: str):
        """insertion sort para diccionario segun el campo offset"""
        for i in range(1, len(frags)):
            actual = frags[i]
            j = i-1
            while j >= 0 and frags[j][campo] > actual[campo]:
                frags[j + 1] = frags[j]
                j -= 1

            frags[j + 1] = actual


    @staticmethod
    def fragment_IP_packet(IP_packet: bytes, MTU: int) -> list[dgrama.Dgram]:
        if len(IP_packet) <= MTU:
            mensaje = dgrama.Dgram(IP_packet)
            mensaje.header_dict["offset"] = 0
            return [mensaje]

        fragmentacion = []
        dict_segmento = dgrama.Dgram.parse_packet(IP_packet)
        msg_bytes = dict_segmento["msg"].encode()

        #tamaño de header será siempre 15B, entonces el mensaje solo se 
        #podra enviar de a cada (MTU -15)B
        delta_msg = MTU - 15
        offset_frag = 0     #offset empieza en 0
        while msg_bytes:
            msg_frag = msg_bytes[:delta_msg]
            msg_bytes = msg_bytes[delta_msg:]   #actualizacion inmediata del buufer del mensaje
            dict_msg_frag = {
                "ip": dict_segmento["ip"],
                "port": dict_segmento["port"],
                "ttl": dict_segmento["ttl"],
                "id": dict_segmento["id"],
                "offset": offset_frag,
                "size": len(msg_bytes),
                "flag": 1 if msg_bytes else 0,  #detecta automaticamente si hay mas contenido
                "msg": msg_frag.decode()
            }
            #envuelto en el header, se inicializa un Dgram
            msg_frag_wrapped = dgrama.Dgram.create_packet(dict_msg_frag)
            dgram_fragment = dgrama.Dgram(msg_frag_wrapped)
            fragmentacion.append(dgram_fragment)

            offset_frag += len(msg_frag)

        return fragmentacion


    def reassemble_IP_packet(self, fragment_list: list[dgrama.Dgram]) -> dgrama.Dgram:
        number_of_frag = len(fragment_list)
        msg_segmento = ""
        msg_size = 0
        segmento_ip = fragment_list[0].header_dict["ip"]
        segmento_port = fragment_list[0].header_dict["port"]
        segmento_ttl = fragment_list[0].header_dict["ttl"]
        segmento_id = fragment_list[0].header_dict["id"]
        segmento_offset_inicial = fragment_list[0].header_dict["offset"]

        if number_of_frag == 1:
            if (fragment_list[0]["flag"]) or (fragment_list[0]["offset"] > 0):
                print("[ERROR] Lista no valida")
                return None

            else:
                print("Paquete retornado con mensaje:" \
                f"{fragment_list[0]["msg"]}\n")
                return fragment_list[0]

        else:
            #ordenamos lista segun offset
            Router.insertion_sort_fragments(fragment_list, "offset")
            offset = segmento_offset_inicial #primer offset esperado, se va acumulando
            for fragment in fragment_list:
                if not fragment.header_dict["id"] == segmento_id:
                    print("[ERROR] ID de segmento no calza")
                    return None

                if fragment.header_dict["offset"] == offset:
                    segmento_ttl = max(segmento_ttl, fragment.header_dict["ttl"])
                    msg_segmento += fragment.header_dict["msg"]
                    msg_size += fragment.header_dict["size"]
                    #proximo offset
                    offset += (fragment.header_dict["size"] + 1)

                    if fragment.header_dict["flag"] == 0:
                        dict_segment = {
                            "ip": segmento_ip,
                            "port": segmento_port,
                            "ttl": segmento_ttl,
                            "id": segmento_id,
                            "offset": segmento_offset_inicial,
                            "size": msg_size,
                            "flag": 0,   #se retorna como 0, s necesecita en 1 se maneja fuera de la funcion
                            "msg": msg_segmento
                        }

                        return dgrama.Dgram(dgrama.Dgram.create_packet(dict_segment))

                else:
                    print("[ERROR] Segmento incompleto descartado")
                    return None
        


         



    def check_routes(self, destination_address: tuple[str, int], debug = False) -> tuple[tuple[str, int], int]:

        for linea in self.rt_table:
            linea_split = linea.split(" ")
            ip_linea = linea_split[0].split("/")[0] #no tomamos en cuenta mascara
            #calzar ip
            if destination_address[0] == ip_linea:
                puerto_dest = destination_address[1]
                if puerto_dest >= int(linea_split[1]) and puerto_dest <= int(linea_split[2]):

                    #round-robin
                    self.rt_table.remove(linea)
                    self.rt_table.append(linea)
                    if debug:
                        print(f"[DEBUG] Nueva tabla de rutas para {self.name}")
                        self.print_table()

                    next_hop = (linea_split[3], int(linea_split[4])) 

                    return (next_hop, int(linea_split[5]))

        return None

    

    def recv_segment(self):
        segment, desde = self.rt_socket.recvfrom(1024) 
        print(f"###### {self.name} ######")
        segment_dgram = dgrama.Dgram(segment) #con esto ya tenemos header(segmento) y diccionario del mensaje, sirve para tomar desiciones

        if segment_dgram.header_dict["ttl"] <= 0:
            print("Se recibió paquete con TTL = 0\n")
            return

        segment_dest = (segment_dgram.header_dict["ip"], segment_dgram.header_dict["port"])
             
        #si es el router de destino o por defecto
        if segment_dest[0] == self.bind_ad[0] and segment_dest[1] == self.bind_ad[1]:
            print(f"Fragmento recibido desde {desde}:")
            print(f"ID de mensaje: {segment_dgram.header_dict["id"]}")
            print(f"Offset de fragmento: {segment_dgram.header_dict["offset"]}")
            print(f"Tamaño del fragmento: {segment_dgram.header_dict["size"]}")
            print(f"Ultimo?: {not segment_dgram.header_dict["flag"]}")

        else: 
            next_hop_MTU = self.check_routes(segment_dest)
            if next_hop_MTU == None:
                #descartado
                print(f"[ERROR] No hay rutas hacia {segment_dest} => DESCARTADO\n")
                    
            else:
                print(f"[INFO] Redirigiendo paquete con destino final {segment_dest} desde {self.bind_ad} hacia {next_hop_MTU[0]} con MTU: {next_hop_MTU[1]}\n")
                lista_de_fragmentos = Router.fragment_IP_packet(segment, next_hop_MTU[1])

                for fragmento in lista_de_fragmentos:
                    self.send_pack(fragmento, next_hop_MTU[0])
                    time.sleep(1)




    @staticmethod
    def main(bind_ad: tuple[str, int], filename: str):
        router = Router(bind_ad, filename)

        #ciclo de recepcion de mensajes
        while True:
            router.recv_segment()



if __name__ == "__main__":
    bind_ad_r = ("127.0.0.1", 5000)
    Router.main(bind_ad_r, "R1")


    





