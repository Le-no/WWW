import socket
import http_utils as hu
from pathlib import Path
import os
import urllib.parse
from urllib.parse import unquote

HOST, PORT = 'localhost', 8888

def get_subdirs(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def get_files(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isfile(os.path.join(a_dir, name))]

def starting(top):
    dir = ''
    for name in get_subdirs(top):
        dir += '<li class="list-group-item"><span class="fa fa-folder"></span><a class="pl-3" href="/' + urllib.parse.urljoin(top + '/', name) + '">' + name + "</a></li>"
    for name in get_files(top):
        dir += '<li class="list-group-item"><span class="fa fa-file"></span><span class="pl-3">' + name + "</span></li>"
    return dir

def send_fail(conn, status_code, msg):
    header, response = hu.make_response(status_code, {}, msg)
    conn.send(header + response)
    conn.close()

def send_html(conn, html):
    htmlBytes = html.encode('utf-8')
    headers = {
        'Content-Type': 'text/html; charset=UTF-8',
        'Content-Length': str(len(htmlBytes))
    }
    header, response = hu.make_response(200, headers, htmlBytes)
    conn.send(header + response)
    conn.close()

def read_to_end(conn):
    buffer = bytearray()
    buffSz = 1024
    while True:
        data = conn.recv(buffSz)
        if data:
            buffer.extend(data)
        else:
            break
        if len(data) < buffSz:
            break
    return buffer

def create_html(content):
    return """<html>
<head>
    <title>File Listing</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha256-YLGeXaapI0/5IgZopewRJcFXomhRMlYYjugPLSyNjTY=" crossorigin="anonymous" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.11.2/css/all.min.css" integrity="sha256-+N4/V/SbAFiW1MPBCXnfnP9QSN3+Keu+NlB+0ev/YKQ=" crossorigin="anonymous" />
</head>
<body>
<div class="row mt-3">
<div class="container">""" + content +  """
</div>
</div>
</body>
                    </html>"""

def handle_connection(conn):
    req = read_to_end(conn)
    try:
        request_data = hu.decode_http(req)
        method = request_data['Request'].split()[0]
        if method.lower() != 'get':
            send_fail(conn, 501, "Not Implemented")
            return
        if not request_data.get('Host'):
            send_fail(conn, 400, "Bad Request")
            return


        pathString = "." + unquote(request_data["Request"].split()[1])
        if not os.path.isdir(pathString):
            send_fail(conn, 404, "Not Found")
            return
        if ".." in pathString:
            send_fail(conn, 403, "Forbidden")
            return
        path = Path(pathString)
        parent = path.parent
        string = starting(pathString)
    except Exception as e:
        print(e)
        send_fail(conn, 500, "Internal Server Error")
        return

    content = "".join([
        '<ul class="list-group-item list-group-item-secondary">',
        '<a href="/',
        str(parent),
        '">Go Up</a></ul>',
        string
    ])

    html = create_html(content)
    send_html(conn, html)

def main():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((HOST, PORT))
    listen_socket.listen(1)

    while True:
        conn, _ = listen_socket.accept()
        with conn:
            handle_connection(conn)

main()