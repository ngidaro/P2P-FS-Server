import pickle
import os

def download(parsed_msg, connection):
    downloadfile = parsed_msg[2]
    downloadfilepath = os.path.abspath(downloadfile)

    if downloadfilepath != '':
        serializeddownloadfile = SerializeFiles(downloadfilepath)
        connection.sendall(serializeddownloadfile)
        return 'FILE SENT SUCCESSFULLY:' + parsed_msg[1]  # Add filename, chunk text
    else:
        return 'DOWNLOAD ERROR: ' + parsed_msg[1] + 'FILE NOT FOUND'


def SerializeFiles(f):
    allfilecontent=[]
    fil=open(f, 'r')
    content = fil.readlines()
    allfilecontent += content
    return pickle.dumps(content)
