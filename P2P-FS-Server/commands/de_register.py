from Client import Client


def de_register(parsed_msg, clients):
    if len(parsed_msg) == 3:
        rq = parsed_msg[1]
        name = parsed_msg[2]

        for index, client in enumerate(clients):
            if name == client.name:
                # Remove this client from the list
                clients.pop(index)
                return 'DE-REGISTERED | ' + rq + ' | ' + name

        return ''
    else:
        return 'Invalid Command'
