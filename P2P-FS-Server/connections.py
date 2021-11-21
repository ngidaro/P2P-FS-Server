import socket
import pickle
import sys
import parse_commands as pc


def startUDP(HOST, PORT, remote_HOST, remote_PORT):
    clients = []

    # UDP Server - Create UDP Datagram socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket Created')
    except socket.error:
        print('Failed to create socket.')
        sys.exit()

    # Bind socket
    try:
        s.bind((HOST, PORT))
        sock.bind(('', 10000))
        sock.listen(1)


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
                msg_to_client = pc.get_data(data, clients, sock)

                s.sendto(str.encode(msg_to_client), addr)
                print('Message[' + addr[0] + ':' + str(addr[1]) + '] ' + data.strip())

                # Save a copy of clients to the backup server
                clients_data = pickle.dumps(clients)
                s.sendto(clients_data, (remote_HOST, remote_PORT))
    sock.close()
    s.close()
