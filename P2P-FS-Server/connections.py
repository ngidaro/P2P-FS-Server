import socket
import select
import threading
import pickle
import sys
import parse_commands as pc
from commands.publish import publish
from commands.backupData import saveData, restoreData, restoreSocketList, saveSocketData


def readTCPMessage(clientSocket):
    try:
        clientMessage = clientSocket.recv(1024)

        if not len(clientMessage):
            return False

        return clientMessage
    except Exception:
        return False


def TCPConnectionThread(TCP_Port, clients):
    socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    socketTCP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socketTCP.bind(('', TCP_Port))
    print('TCP Socket Bind Complete')

    socketTCP.listen()

    # Array containing all the sockets to pay attention to
    # socketsList = [socketTCP]
    socketsList = restoreSocketList("socketsListBackup")
    if not socketsList:
        socketsList.append(socketTCP)
    # socketsList = [socketTCP] + restoreData("socketsListBackup")

    while True:
        # -------------- Backup Data to File --------------
        # Need to save the clientSocket so that when server boots up, it knows what to lookout for
        saveSocketData("socketsListBackup", socketsList)
        saveData("clientsBackup", clients)
        # -------------- End of Backup --------------

        readable, _, errors = select.select(socketsList, [], socketsList)
        for socketNotified in readable:
            # if socketNotified is the server socket, then there is a new connection pending
            if socketNotified == socketTCP:
                # Accept new connection
                clientSocket, clientAddress = socketNotified.accept()

                # Initial message sent by Client (contains client's name)
                clientMessage = readTCPMessage(clientSocket).decode()

                if clientMessage is False:
                    continue

                # Add socket to the list of connected sockets
                socketsList.append(clientSocket)

                # Need to save clientSocket in Client array
                # First message sent from client is the client's name
                print(f"TCP Connection from {clientAddress}")
            else:
                # This is where the PUBLISH happens
                clientData = readTCPMessage(socketNotified)

                # Connection closed on client side
                if clientData is False:
                    socketsList.remove(socketNotified)
                    # saveData("socketsListBackup", socketsList)
                    continue

                # -------------- Do Publish Here --------------
                data = pickle.loads(clientData)

                # data[0]: Client input string
                # data[1]: files
                sPublishedMsg = publish(clients, data[0].split(' '), data[1])

                print(sPublishedMsg)
                # Send the return message back to the client
                socketNotified.send(sPublishedMsg.encode())
                # -------------- End of Publish --------------

                # Save copy to files:
                # saveData("clientsBackup", clients)
                # saveData("socketsListBackup", socketsList)

        for socketNotified in errors:
            socketsList.remove(socketNotified)
            # Save socketsList
            # saveData("socketsListBackup", socketsList)


def startUDP(HOST, PORT, remote_HOST, remote_PORT, TCP_Port):
    clients = restoreData("clientsBackup")

    # UDP Server - Create UDP Datagram socket
    try:
        socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print('UDP Socket Created')
    except socket.error:
        print('Failed to create socket.')
        sys.exit()

    # Bind socket
    try:
        socketUDP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socketUDP.bind((HOST, PORT))
        print('UDP Socket Bind Complete')
    except socket.error:
        print('Bind Failed')
        sys.exit()

    # Start TCP thread
    threading.Thread(target=TCPConnectionThread, args=[TCP_Port, clients]).start()

    # if the "other" server is running, then send the client data from that backup server to here
    # Command sent on server startup will be REQUEST_BACKUP
    # socketUDP.sendto(str.encode('REQUEST_BACKUP'), (remote_HOST, remote_PORT))

    # Infinite Loop for UDP
    # This handles all messages sent using UDP
    while True:
        clientData = ''
        d = socketUDP.recvfrom(1024)
        try:
            clientData = str(d[0].decode())
            clientAddress = d[1]  # (client address, client port number)
            if not clientData:
                break
        except UnicodeDecodeError:
            # Will execute this if there is a decode error -> data passed is an array
            # Copies data from "other" server to this one
            clients = pickle.loads(d[0])

        if clientData:
            # if the command is REQUEST_BACKUP then the server will send the clients data to the backup server
            if clientData.split(' ')[0] == 'REQUEST_BACKUP':
                # send client data to server
                clients_data = pickle.dumps(clients)
                socketUDP.sendto(clients_data, (remote_HOST, remote_PORT))
            else:
                msg_to_client = pc.get_data(clientData, clients)

                socketUDP.sendto(str.encode(msg_to_client), clientAddress)
                print('Message[' + clientAddress[0] + ':' + str(clientAddress[1]) + '] ' + clientData.strip())

                # Save a copy of clients to the backup server
                # clients_data = pickle.dumps(clients)
                # socketUDP.sendto(clients_data, (remote_HOST, remote_PORT))
                saveData("clientsBackup", clients)

    socketUDP.close()
