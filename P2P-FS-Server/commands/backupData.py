from pathlib import Path
import pickle
import socket


def restoreData(filename):
    # Restore data if file exists
    if Path(f"backup/{filename}").exists():
        try:
            return pickle.load(open(f"backup/{filename}", "rb"))
        except EOFError as e:
            # Error occurs if the file is empty
            pass
    return []


def saveData(filename, dataArray):
    pickle.dump(dataArray, open(f"backup/{filename}", "wb"))


# Can't save the socket but can save the data {family, type, proto, laddr, raddr}
def saveSocketData(filename, dataArray):
    socketsList = []
    for sock in dataArray:
        socketArguments = {
            'family': sock.family,
            'type': sock.type,
            'proto': sock.proto
        }
        socketsList.append(socketArguments)
    saveData(filename, socketsList)


def restoreSocketList(filename):
    socketsList = []
    socketsListArguments = restoreData(filename)
    for socketArguments in socketsListArguments:
        socketObj = socket.socket(**socketArguments)
        socketsList.append(socketObj)

    return socketsList
