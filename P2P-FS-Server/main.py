from connections import startUDP

# First Server
if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 8888

    TCP_Port = 11111

    startUDP(HOST, PORT, TCP_Port)
