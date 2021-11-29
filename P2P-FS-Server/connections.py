import socket
import select
import threading
import pickle
import sys
import parse_commands as pc
from commands.publish import publish
from commands.backupData import saveData, restoreData, retrieveClientFiles


# ************************************************************
# readTCPMessage:
#   Description: Function which receives TCP data from client
#   Parameters:
#       clientSocket: The client's TCP socket
# ************************************************************


def readTCPMessage(clientSocket):
    try:
        clientMessage = clientSocket.recv(1024)

        if not len(clientMessage):
            return False

        return clientMessage
    except Exception as e:
        return False


# ************************************************************
# handleFile:
#   Description: Function which unloads data from client (TCP) and publishes the file to the client's local directory
#   Parameters:
#       clients: The array of all clients
#       clientData: The client's data passed using TCP (non-decoded)
#       socketNotified: The socket of the client that sent the data to the server
# ************************************************************


def handleFile(clients, clientData, socketNotified):
    data = pickle.loads(clientData)

    # data[0]: Client input string
    # data[1]: files
    if len(data) > 1:
        sPublishedMsg = publish(clients, data[0].split(' '), data[1])
        print(sPublishedMsg)
        # Send the return message back to the client
        socketNotified.send(sPublishedMsg.encode())


# ************************************************************
# TCPConnectionThread:
#   Description: Thread Function which constantly waits and establishes TCP connection with clients.
#         Also handles data passed from the client using TCP socket
#   Parameters:
#       TCP_Port: The server's current TCP port
#       clients: The array of all clients
# ************************************************************


def TCPConnectionThread(TCP_Port, clients):
    socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    socketTCP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socketTCP.bind(('', TCP_Port))
    print('TCP Socket Bind Complete')

    socketTCP.listen()

    # Array containing all the sockets to pay attention to
    socketsList = [socketTCP]

    while True:
        # -------------- Backup Data to File --------------
        saveData("clientsBackup", clients)
        # -------------- End of Backup --------------

        readable, _, errors = select.select(socketsList, [], socketsList)
        for socketNotified in readable:
            # if socketNotified is the server socket, then there is a new connection pending
            if socketNotified == socketTCP:
                # Accept new connection
                clientSocket, clientAddress = socketNotified.accept()

                # Initial message sent by Client
                clientData = readTCPMessage(clientSocket)

                try:
                    clientData.decode()  # If data is not decodable then data is a file dumped by pickle
                    if clientData is False:
                        continue
                except UnicodeDecodeError as e:
                    # If this is the error then the data is dumped by pickle and a file was passed
                    # -------------- Do Publish Here --------------
                    handleFile(clients, clientData, clientSocket)
                    # -------------- End of Publish --------------

                # Add socket to the list of connected sockets
                socketsList.append(clientSocket)

                # First message sent from client is the client's name
                print(f"TCP Connection from {clientAddress}")
            else:
                # This is where the PUBLISH happens
                clientData = readTCPMessage(socketNotified)

                # Connection closed on client side
                if clientData is False:
                    socketsList.remove(socketNotified)
                    continue

                # -------------- Do Publish Here --------------
                handleFile(clients, clientData, socketNotified)
                # -------------- End of Publish --------------

        for socketNotified in errors:
            socketsList.remove(socketNotified)


# ************************************************************
# startUDP:
#   Description: Starts UDP connection and waits for incoming messages from clients
#   Parameters:
#       HOST: The server's Host name
#       PORT: The server's UDP port number
#       TCP_Port: The server's TCP port number
# ************************************************************


def startUDP(HOST, PORT, TCP_Port):
    clients = restoreData("clientsBackup")
    retrieveClientFiles(clients)

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

    # Infinite Loop for UDP
    # This handles all messages sent using UDP
    while True:
        d = socketUDP.recvfrom(1024)
        clientData = str(d[0].decode())
        clientAddress = d[1]  # (client address, client port number)
        if not clientData:
            break

        if clientData:
            msg_to_client = pc.handleClientMessage(clientData, clients, None)

            socketUDP.sendto(str.encode(msg_to_client), clientAddress)
            print('Message[' + clientAddress[0] + ':' + str(clientAddress[1]) + '] ' + clientData.strip())

            # Save a copy of clients to the backup file
            saveData("clientsBackup", clients)

    socketUDP.close()
