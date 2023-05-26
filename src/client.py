import socket

IPADDR = "127.0.0.1"
PORT = 49152

while True:
    try:
        sock = socket.socket(socket.AF_INET)
        sock.connect((IPADDR, PORT))
        break
    except:
        print("server is not active. Attempt to connect again.")


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