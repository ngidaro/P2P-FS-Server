class Client:

    name = ''
    address = ''
    port_UDP = 0
    port_TCP = 0

    # Files uploaded by the Client
    files = []

    def __init__(self, name, address, port_UDP, port_TCP):
        self.name = name
        self.address = address
        self.port_UDP = port_UDP
        self.port_TCP = port_TCP

    def update_client(self, address, port_UDP, port_TCP):
        self.address = address
        self.port_UDP = port_UDP
        self.port_TCP = port_TCP

    # Displays all data for this client
    def display_data(self):
        fileString = ''
        for file in self.files:
            fileString = fileString + ' ' + file

        return self.name + ' ' + self.address + ' ' + str(self.port_TCP) + ' ' + fileString

    # Displays only info for this client not their files (used for SEARCH-FILE)
    def displayInfo(self):
        return self.name + ' ' + self.address + ' ' + str(self.port_TCP)

    # Searches for specific file in files array
    def searchFile(self, filename):
        for file in self.files:
            if file == filename:
                return 1
        return 0

    def addFile(self, filename):
        self.files.append(filename)

    def removeFile(self, file):
        for index, filename in enumerate(self.files):
            if filename == file:
                # Remove this file from the list
                self.files.pop(index)
                return 1

        # File does not exist for this user
        return 0

    def retrieveFiles(self, files):
        self.files = files

    def deleteAllFiles(self):
        del self.files[:]
