import os
import sys
import socket

home_dir = os.path.expanduser('~')
git_dir = os.path.join(home_dir, 'git')

repository_base = os.path.join(git_dir, "brainvision-controller")

workspace_base = os.path.join("D:", "workspace", "simon_kojima")

HOST = socket.gethostname()
IPADDR = socket.gethostbyname(HOST)
PORT = 49152