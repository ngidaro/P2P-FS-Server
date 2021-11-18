import socket
import pickle


def getClientIndex(username, clients):
    for index, client in enumerate(clients):
        if client.name == username:
            return index
    # if the client does not exist
    return -1


def publish(parsed_msg, clients):
    if len(parsed_msg) > 3:
        # -----------Open TCP socket for passing text files-----------
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('', 10000)

        sock.bind(server_address)

        sock.listen(1)
        # ----------------------------------------------------------
        publishedfiles = parsed_msg[3:]

        # Get the clients index so that we can eventually add the files to their array of files
        clientIndex = getClientIndex(parsed_msg[2], clients)
        if clientIndex == -1:
            return 'PUBLISHED-DENIED ' + parsed_msg[1] + ' User does not exist'

        connection, client_address = sock.accept()
        unpickdata = connection.recv(1024)
        data = pickle.loads(unpickdata)
        for file in publishedfiles:
            f = open('public/' + file, "a")

            # Add filename to clients array of uploaded files
            clients[clientIndex].addFile(file)

            count = 0
            for element in data:
                if element == "01111110":
                    if count == 0:
                        pass
                        count += 1
                    else:
                        count += 1
                        break
                else:
                    f.write(element)
                    count += 1
            f.close()
            data = data[count:]

        connection.close()
        return 'PUBLISHED ' + parsed_msg[1]
    else:
        return 'PUBLISHED-DENIED ' + parsed_msg[1] + ' Missing parameters'


# def startTCP(filename):
#     while True:
#         try:
#             print(sys.stderr, 'connection from', client_address)
#             while True:
#                 data = connection.recv(1024)
#                 f.write(pickle.loads(data))
#                 if not data:
#                     break
#         finally:
#             connection.close()
#         f.close()
