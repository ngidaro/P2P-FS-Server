from connections import startUDP

# Second Server
if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 3000

    TCP_Port = 22222

    startUDP(HOST, PORT, TCP_Port)
