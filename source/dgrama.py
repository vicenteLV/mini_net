import socket

"""
header :: IP(4bytes);Puerto(2bytes);mensaje"""


class Dgram:

    def __init__(self):
        self.socket : socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.header : bytes = None
        self.header_dict : dict = None 
