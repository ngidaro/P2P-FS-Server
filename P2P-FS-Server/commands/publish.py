import socket
import pickle
import sys
def publish(parsed_msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('', 10000)

    sock.bind(server_address)


    publishedfiles=parsed_msg[3:]
    sock.listen(1)
    connection, client_address = sock.accept()
    unpickdata = connection.recv(1024)
    data=pickle.loads(unpickdata)
    for file in publishedfiles:
        f = open(file, "a")
        count=0
        for element in data:
            if element=="01111110":
                if count==0:
                    pass
                    count+=1
                else:
                    count+=1
                    break
            else:
                f.write(element)
                count+=1
        f.close()
        data=data[count:]
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