from Client import Client


def register(parsed_msg, clients):
    if len(parsed_msg) == 6:
        rq = parsed_msg[1]
        name = parsed_msg[2]
        IP_address = parsed_msg[3]
        port_UDP = int(parsed_msg[4])
        port_TCP = int(parsed_msg[5])

        # Check if the name doesn't exist already in the list of clients
        for client in clients:
            if name == client.name:
                return 'REGISTER-DENIED ' + rq + ' Username has already been taken'

        # Add new client to array
        clients.append(Client(name, IP_address, port_UDP, port_TCP))

        return 'REGISTERED ' + rq
    else:
        return 'REGISTER-DENIED ' + parsed_msg[1] + ' Invalid Command'
