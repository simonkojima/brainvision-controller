import socket
import control
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--emu', action='store_true')
args = parser.parse_args()

if args.emu:
    print("Emulator Mode")
    rec = control.recorder_emu()
else:
    rec = control.ole_recorder()

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
            data = data.decode("utf-8")
            print(data)
            if data.startswith("open"):
                pass
            elif data.startswith("stop_recording"):
                rec.stop_recording() 
            elif data.startswith("stop_viewing"):
                rec.stop_viewing()
            elif data.startswith("load_workspace"):
                try:
                    workspace = data.split(' ')[1]
                    rec.load_workspace(workspace)
                except:
                    print("Error : workspace could not be pursed.")
            elif data.startswith("start_viewing"):
                rec.start_viewing()
            elif data.startswith("start_recording"):
                file = data.split(' ')[1]
                rec.start_recording(file)
            elif data.startswith("stop_recording"):
                rec.stop_recording()
            elif data.startswith("initialize_recorder"):
                try:
                    workspace = data.split(' ')[1]
                    rec.initialize_recorder(workspace)
                except:
                    print("Error : workspace could not be pursed.")
            else:
                print("Unknown command '%s' was recieved" %str(data))

            #print(data.decode("utf-8"))
        except ConnectionResetError:
            print("Error")
            break
    print("closed")
    
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
                val = input("The connection was closed. Do you want wait for a new connection?. [y]/n : ")
                if val == 'y' or val == '':
                    break
                elif val == 'n':
                    exit()
                else:
                    continue
        except TimeoutError:
            pass
        #except:
        #    print("error")
        #    #exit()
