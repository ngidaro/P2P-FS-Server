from commands.register import register
from commands.de_register import de_register
from commands.publish import publish
from commands.remove import remove
from commands.retrieve_all import retrieve_all
from commands.retrieve_infot import retrieve_infot
from commands.search_file import search_file
from commands.download import download
from commands.update_contact import update_contact

REGISTER = 'REGISTER'
DEREGISTER = 'DE-REGISTER'
PUBLISH = 'PUBLISH'
REMOVE = 'REMOVE'
RETRIEVEALL = 'RETRIEVE-ALL'
RETRIEVEINFOT = 'RETRIEVE-INFOT'
SEARCHFILE = 'SEARCH-FILE'
DOWNLOAD = 'DOWNLOAD'
UPDATECONTACT = 'UPDATE-CONTACT'


def get_data(msg, addr, clients):
    commands = [REGISTER, DEREGISTER, PUBLISH, REMOVE, RETRIEVEALL, RETRIEVEINFOT, SEARCHFILE, DOWNLOAD, UPDATECONTACT]

    parsed_msg = msg.split(' ')

    # TODO: Validation of the registered user needs to be done in here

    # Check to make sure a command was given
    if parsed_msg[0] in commands:
        # If new user is being registered, we need to save the client address and port numbers
        if parsed_msg[0] == REGISTER:
            return_msg = register(parsed_msg, clients)
        elif parsed_msg[0] == DEREGISTER:
            return_msg = de_register(parsed_msg, clients)
        elif parsed_msg[0] == PUBLISH:
            return_msg = publish(parsed_msg)
        elif parsed_msg[0] == REMOVE:
            return_msg = remove(parsed_msg)
        elif parsed_msg[0] == RETRIEVEALL:
            return_msg = retrieve_all(parsed_msg, clients)
        elif parsed_msg[0] == RETRIEVEINFOT:
            return_msg = retrieve_infot(parsed_msg)
        elif parsed_msg[0] == SEARCHFILE:
            return_msg = search_file(parsed_msg)
        elif parsed_msg[0] == DOWNLOAD:
            return_msg = download(parsed_msg)
        elif parsed_msg[0] == UPDATECONTACT:
            return_msg = update_contact(parsed_msg, clients)
        else:
            return_msg = 'Invalid Command'
    else:
        return_msg = 'Invalid Command'

    return return_msg
