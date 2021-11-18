from commands.publish import getClientIndex
from pathlib import Path


def remove(parsed_msg, clients):
    if len(parsed_msg) > 3:
        filesToRemove = parsed_msg[3:]

        # Gets the index of the client in the array of clients
        clientIndex = getClientIndex(parsed_msg[2], clients)
        if clientIndex == -1:
            return 'REMOVE-DENIED ' + parsed_msg[1] + ' User does not exist'

        # Removes the files from 'public' directory
        for file in filesToRemove:
            fileToRemove = Path("public/" + parsed_msg[2] + '/' + file)
            # Check to see if the file exists in the public directory
            if fileToRemove.is_file():
                # Removes the file from the clients array of files
                if clients[clientIndex].removeFile(file):
                    # Remove the file from /public
                    fileToRemove.unlink()
                else:
                    return 'REMOVED-DENIED ' + parsed_msg[1] + ' Cannot remove file that does not belong to ' + parsed_msg[2]

            else:
                return 'REMOVED-DENIED ' + parsed_msg[1] + ' File ' + file + ' does not exist'

        return 'REMOVED ' + parsed_msg[1]
    else:
        return 'REMOVED-DENIED ' + parsed_msg[1] + ' Missing Parameters'
