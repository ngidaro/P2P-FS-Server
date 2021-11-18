def search_file(parsed_msg, clients):
    if len(parsed_msg) == 3:
        returnMsg = ''
        for client in clients:
            if client.searchFile(parsed_msg[2]):
                returnMsg = returnMsg + client.displayInfo() + ' | '

        if returnMsg:
            return 'SEARCH-FILE ' + parsed_msg[1] + ' ' + returnMsg
        else:
            return 'SEARCH-ERROR ' + parsed_msg[1] + ' File does not exist'
    else:
        return 'SEARCH-ERROR ' + parsed_msg[1] + ' Invalid number of parameters'
