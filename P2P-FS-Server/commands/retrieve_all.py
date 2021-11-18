def retrieve_all(parsed_msg, clients):
    if len(parsed_msg) == 2:
        return_msg = 'RETRIEVE ' + parsed_msg[1] + ' |'
        for client in clients:
            return_msg += ' (' + client.display_data() + ') |'
        return return_msg
    return 'Invalid Command'
