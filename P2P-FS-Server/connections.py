import socket
import pickle
import sys
import parse_commands as pc


def startUDP(HOST, PORT, remote_HOST, remote_PORT):
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

    # if the "other" server is running, then send the client data from that backup server to here
    # Command sent on server startup will be REQUEST_BACKUP
    s.sendto(str.encode('REQUEST_BACKUP'), (remote_HOST, remote_PORT))

    while 1:
        data = ''
        d = s.recvfrom(1024)
        try:
            data = str(d[0].decode())
            addr = d[1]  # (client address, client port number)
            if not data:
                break
        except UnicodeDecodeError:
            # Will execute this if there is a decode error -> data passed is an array
            # Copies data from "other" server to this one
            clients = pickle.loads(d[0])

        if data:
            # if the command is REQUEST_BACKUP then the server will send the clients data to the backup server
            if data.split(' ')[0] == 'REQUEST_BACKUP':
                # send client data to server
                clients_data = pickle.dumps(clients)
                s.sendto(clients_data, (remote_HOST, remote_PORT))
            else:
                # Parse the data
                msg_to_client = pc.get_data(data, clients)

                s.sendto(str.encode(msg_to_client), addr)
                print('Message[' + addr[0] + ':' + str(addr[1]) + '] ' + data.strip())

                # Save a copy of clients to the backup server
                clients_data = pickle.dumps(clients)
                s.sendto(clients_data, (remote_HOST, remote_PORT))

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
                print(sys.stderr, 'received "%s"' % data)
                if data:
                    print(sys.stderr, 'sending data back to the client')
                    connection.sendall(data)
                else:
                    print(sys.stderr, 'no more data from', client_address)
                    break
        finally:
            connection.close()
