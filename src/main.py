import socket
import threading

IPADDR = "127.0.0.1"
PORT = 49152

sock_sv = socket.socket(socket.AF_INET)
sock_sv.settimeout(5)
sock_sv.bind((IPADDR, PORT))
sock_sv.listen()

def recv_client(sock, addr):
    while True:
        try:
            data = sock.recv(1024)
            if data == b"":
                break
            print(data.decode("utf-8"))
        except ConnectionResetError:
            break
    
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

if __name__ == "__main__":
    while True:
        try:
            print("waiting for a new connection....")
            sock_cl, addr = sock_sv.accept()
            print("connected : %s" %str(addr))
            recv_client(sock_cl, addr)
            while True:
                val = input("Connection was closed. Do you want to continue?. [y]/n : ")
                if val == 'y':
                    break
                elif val == 'n':
                    exit()
                else:
                    continue
        except TimeoutError:
            pass
        except:
            exit()
