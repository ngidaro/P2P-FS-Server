from connections import startUDP

# First Server
if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 8888

    # The following is the IP and port of the second server
    remote_HOST = '0.0.0.0'
    remote_PORT = 3000

    startUDP(HOST, PORT, remote_HOST, remote_PORT)

