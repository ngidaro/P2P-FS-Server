import pickle
import os


def download(parsed_msg, connection):
    downloadFile = parsed_msg[2]
    downloadFilePath = os.path.abspath(downloadFile)

    if os.path.exists(downloadFilePath):
        serializedDownloadFile = serializeFiles(downloadFilePath)
        connection.sendall(serializedDownloadFile)
        return 'FILE SENT SUCCESSFULLY:' + parsed_msg[1]  # Add filename, chunk text
    else:
        return 'DOWNLOAD-ERROR: ' + parsed_msg[1] + ' FILE NOT FOUND'


def serializeFiles(filename):
    allFileContent = []
    file = open(filename, 'r')
    content = file.readlines()
    allFileContent += content
    return pickle.dumps(content)
