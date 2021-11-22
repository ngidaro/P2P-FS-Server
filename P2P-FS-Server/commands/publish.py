import socket
import pickle
from pathlib import Path


def getClientIndex(username, clients):
    for index, client in enumerate(clients):
        if client.name == username:
            return index
    # if the client does not exist
    return -1


def publish(parsed_msg, clients, connection):
    if len(parsed_msg) > 3:
        # -----------Open TCP socket for passing text files-----------


        # ----------------------------------------------------------
        publishedfiles = parsed_msg[3:]

        # Get the clients index so that we can eventually add the files to their array of files
        clientIndex = getClientIndex(parsed_msg[2], clients)
        if clientIndex == -1:
            return 'PUBLISHED-DENIED ' + parsed_msg[1] + ' User does not exist'

        #connection, client_address = sock.accept()
        unpickdata = connection.recv(1024)
        data = pickle.loads(unpickdata)

        for file in publishedfiles:

            # Check if client's folder exists, if it doesn't then make one
            clientFolder = Path("public/" + parsed_msg[2])
            if not clientFolder.exists():
                clientFolder.mkdir(parents=True)

            f = open('public/' + parsed_msg[2] + '/' + file, "a")

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
        return 'PUBLISHED ' + parsed_msg[1]
    else:

        return 'PUBLISHED-DENIED ' + parsed_msg[1] + ' Missing parameters'

