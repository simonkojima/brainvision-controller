import socket

IPADDR = "127.0.0.1"
PORT = 49152

sock = socket.socket(socket.AF_INET)
sock.connect((IPADDR, PORT))

while True:
    data = input("> ")
    if data == "exit":
        break
    else:
        try:
            sock.send(data.encode("utf-8"))
        except ConnectionResetError:
            break

sock.shutdown(socket.SHUT_RDWR)
sock.close()