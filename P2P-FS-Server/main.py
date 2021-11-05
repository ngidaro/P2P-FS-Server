import socket
import sys
import parse_commands as pc


def start_connection():
    HOST = '0.0.0.0'
    PORT = 8888

    clients = []

    # UDP Server - Create UDP Datagram socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print('Socket Created')
    except socket.error:
        print('Failed to create socket.')
        sys.exit()

    # Bind socket
    try:
        s.bind((HOST, PORT))
    except socket.error:
        print('Bind Failed')
        sys.exit()

    print('Socket bind complete')

    while 1:
        d = s.recvfrom(1024)
        data = str(d[0].decode())
        addr = d[1]

        if not data:
            break

        # Parse the data
        msg_to_client = pc.get_data(data, addr, clients)

        s.sendto(str.encode(msg_to_client), addr)
        print('Message[' + addr[0] + ':' + str(addr[1]) + '] ' + data.strip())

    s.close()

def startTCP():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 10010))
    server_address = ('localhost', 10000)

    print(sys.stderr, 'starting up on %s port %s' % server_address)
    sock.bind(server_address)

    sock.listen(1)

    while True:
        print(sys.stderr, 'Waiting for a connection')
        connection, client_address = sock.accept()
        try:
            print(sys.stderr, 'connection from', client_address)
            while True:
                data = connection.recv(16)
                print(sys.stderr, 'recieved "%s"' % data)
                if data:
                    print(sys.stderr, 'sending data back to the client')
                    connection.sendall(data)
                else:
                    print(sys.stderr, 'no more data from', client_address)
                    break
        finally:
            connection.close()

if __name__ == '__main__':
    start_connection()
    startTCP()
