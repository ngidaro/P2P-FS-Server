import pickle
import os


def download(parsed_msg, connection):
    fileInfo = parsed_msg[2].split('/')

    # fileInfo[0]: Client to download from
    # fileInfo[1]: File to download

    if len(fileInfo) != 2:
        return f"DOWNLOAD-ERROR {parsed_msg[1]} FILE NOT FOUND"

    downloadFilePath = f"public/{fileInfo[0]}/{fileInfo[1]}"

    if os.path.exists(downloadFilePath):
        serializedDownloadFile = serializeFile(downloadFilePath)
        connection.sendall(serializedDownloadFile)
        return 'FILE SENT SUCCESSFULLY:' + parsed_msg[1]  # Add filename, chunk text
    else:
        return f"DOWNLOAD-ERROR {parsed_msg[1]} FILE NOT FOUND"


def serializeFile(filename):
    allFileContent = []
    file = open(filename, 'r')
    content = file.readlines()
    allFileContent += content
    return pickle.dumps(content)
