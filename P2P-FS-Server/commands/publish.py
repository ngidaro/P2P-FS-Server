import socket
import pickle
import sys
def publish(parsed_msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('', 10000)

    sock.bind(server_address)

    sock.listen(1)
    connection, client_address = sock.accept()

    publishedfiles=parsed_msg[3:]
    for file in publishedfiles:
        f = open(file, "a")
        while True:
            data = connection.recv(1024)
            try:
                for element in pickle.loads(data):
                    f.write(element)
            except EOFError:
                f.close()
                break
        f.close()
    connection.close()
    return 'PUBLISHED ' + parsed_msg[1]


# def startTCP(filename):
#
#
#     while True:
#
#
#         try:
#             print(sys.stderr, 'connection from', client_address)
#             while True:
#                 data = connection.recv(1024)
#                 f.write(pickle.loads(data))
#                 if not data:
#                     break
#         finally:
#             connection.close()
#         f.close()