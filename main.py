import socket
import http_utils as hu
from directory_utils import starting

HOST, PORT = 'localhost', 8888

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)

while True:
    client_connection, client_address = listen_socket.accept()
    request_data = hu.decode_http(client_connection.recv(1024))
    try:
        path = "." + request_data["Request"].split()[1]
        print(request_data["Request"].split()[1])
        string = starting(path)
    except:
        # TODO Exception
        string = ""
        # print("___Exception!___")

    html = "".join(['<html>',
                    '<head>',
                    '   <title>Search results</title>',
                    '</head>',
                    '<body>',
                    # TODO Back button doesn't work
                    "<a href='..'>Go back</a><br/><br/>",
                    string,
                    '</body>',
                    '</html>'])

    header, response = hu.make_response(200, {}, html)
    client_connection.send(header + response)
    client_connection.close()
