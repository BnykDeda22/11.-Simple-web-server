import socket
from threading import Thread
from datetime import datetime

def server():
    sock = socket.socket()
    try:
        sock.bind(('', 70))
        print("Using port 70")
    except OSError:
        sock.bind(('', 7070))
        print("Using port 7070")
    sock.listen(5)
    while True:
        conn, addr = sock.accept()
        print("Connected", addr)
        thread = Thread(target=web_page, args=(conn, addr,))
        thread.start()

def web_page(conn, addr):
    resp = f'HTTP/1.1 200 OK\n\
        Server: SelfMadeServer v0.0.1\n\
        Date: {datetime.now()}\n\
        Content-Type: text/html\n\
        Connection: close\n\n'
    user = conn.recv(1024).decode()
    path = user.split(" ")[1]
    if path == '/' or path == '/GitHub.html':
        with open('GitHub.html', 'rb') as file:
            answer = file.read()
            conn.send(resp.encode('utf-8') + answer)
    else:
        conn.send(("""HTTP/1.1 Page not found. Error: 404""").encode('utf-8'))

if __name__ == "__main__":
    server()
