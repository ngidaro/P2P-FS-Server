from commands.publish import getClientIndex


def retrieve_infot(parsed_msg, clients):
    if len(parsed_msg) == 3:
        clientIndex = getClientIndex(parsed_msg[2], clients)
        if clientIndex == -1:
            return 'RETRIEVE-ERROR ' + parsed_msg[1] + ' User does not exist'

        return 'RETRIEVE-INFOT ' + parsed_msg[1] + ' ' + clients[clientIndex].display_data()
    else:
        return 'RETRIEVE-ERROR ' + parsed_msg[1] + ' Invalid number of parameters'
