from connections import startUDP

# Second Server
if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 3000

    # The following is the IP and port of the first server
    remote_HOST = '0.0.0.0'
    remote_PORT = 8888

    startUDP(HOST, PORT, remote_HOST, remote_PORT)
    # startTCP()
