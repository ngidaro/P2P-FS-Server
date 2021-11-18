from pathlib import Path


def de_register(parsed_msg, clients):
    if len(parsed_msg) == 3:
        rq = parsed_msg[1]
        name = parsed_msg[2]

        for index, client in enumerate(clients):
            if name == client.name:
                # Remove the files from the public directory related to this client
                for file in client.files:
                    fileToRemove = Path("public/" + file)
                    # Check to see if the file exists in the public directory
                    if fileToRemove.is_file():
                        # Remove the file from /public
                        fileToRemove.unlink()

                # Remove this client from the list
                clients.pop(index)
                return 'DE-REGISTERED ' + rq + ' ' + name

        return ''
    else:
        return 'Invalid Command'
