class Client:

    name = ''
    address = ''
    port_UDP = 0
    port_TCP = 0

    def __init__(self, name, address, port_UDP, port_TCP):
        self.name = name
        self.address = address
        self.port_UDP = port_UDP
        self.port_TCP = port_TCP
