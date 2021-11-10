from Client import Client


def update_contact(parsed_msg, clients):
    if len(parsed_msg) == 6:
        rq = parsed_msg[1]
        name = parsed_msg[2]
        IP_address = parsed_msg[3]
        port_UDP = parsed_msg[4]
        port_TCP = parsed_msg[5]

        for client in clients:
            if name == client.name:
                client.update_client(IP_address, port_UDP, port_TCP)
                return 'UPDATE-CONFIRMED ' + rq + ' ' + name + ' ' + IP_address + ' ' + port_UDP + ' ' + port_TCP

        return 'UPDATE-DENIED ' + parsed_msg[1] + ' ' + parsed_msg[2] + ' ' + 'Name does not exist'
    else:
        if len(parsed_msg) > 2:
            return 'UPDATE-DENIED ' + parsed_msg[1] + ' ' + parsed_msg[2] + ' ' + 'Invalid Parameters'
        else:
            return 'UPDATE-DENIED Invalid Command'
