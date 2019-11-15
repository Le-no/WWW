import socket
from os import listdir, os
from os.path import isfile, join

import http_utils as hu
from directory_utils import makeHTMLtable, starting

HOST, PORT = 'localhost', 8888

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)

while True:
    client_connection, client_address = listen_socket.accept()
    request_data = hu.decode_http(client_connection.recv(1024))
    parent_path = "."
    try:
        path = parent_path + request_data["Request"].split()[1]
        print(request_data["Request"].split()[1])
        string = starting(path)
    except:
        #TODO Exception
        string = ""
        #print("___Exception!___")

    if os.path.isfile(path):
        client_connection..send("EXISTS " + str(os.path.getsize(filename)))
        userResponse = sock.recv(1024)
        if userResponse[:2] == 'OK':
            with open(filename, 'rb') as f:
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)
    else:
        sock.send("ERR ")

    html = "".join(['<html>',
                    '<head>',
                    '   <title>Search results</title>',
                    '</head>',
                    '<body>',
                    "<a href="+ parent_path+">Go back</a><br/><br/>\n",
                    string,
                    '</body>',
                    '</html>'])

    header, response = hu.make_response(200, {}, html)
    client_connection.send(header + response)
    client_connection.close()
