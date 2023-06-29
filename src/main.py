import os
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

IPADDR = "192.168.11.12"
PORT = 49152

sock_sv = socket.socket(socket.AF_INET)
sock_sv.settimeout(5)
sock_sv.bind((IPADDR, PORT))
sock_sv.listen()

def mkdir(dir):
    isExist = os.path.exists(dir)
    if not isExist:
        os.makedirs(dir)

def check_file(file_dir):
    file = os.path.basename(file_dir)
    base = os.path.dirname(file_dir)
    try:
        fname = file.split('.')[0]
        ext = file.split('.')[1]
    except:
        raise ValueError("file should have extension.")
    if os.path.exists(os.path.join(base, file)):
        cnt = 2
        while True:
            new_fname = "%s_%d" %(fname, cnt)
            if os.path.exists(os.path.join(base, fname)):
                cnt += 1
            else:
                return os.path.join(base, "%s.%s"%(new_fname, ext))
    else:
        return os.path.join(base,file)

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
                file = check_file(file)
                print(file)
                rec.start_recording(file)
            elif data.startswith("stop_recording"):
                rec.stop_recording()
            elif data.startswith("initialize_recorder"):
                try:
                    workspace = data.split(' ')[1]
                    rec.initialize_recorder(workspace)
                except:
                    print("Error : workspace could not be pursed.")
            elif data.startswith("mkdir"):
                try:
                    dir = data.split(' ')[1]
                    mkdir(dir)
                except:
                    print("dir was not parsed.")
                    
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
