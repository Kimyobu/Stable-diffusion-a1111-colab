import subprocess
import os.path as Path
import os
import time
import threading
import socket
from .utils import run, py, get_path, get_cwd

WORKSPACE = '/content'

def get_path(path:str):
    return Path.join(WORKSPACE, path)

def check(path:str,isfile=False):
    return Path.isfile(path) if isfile is True else Path.isdir(path)

class A1111:
    def __init__(self,*, cwd=None, file=None, args=None):
        self.cwd = cwd or get_path('A1111')
        self.file = file or get_path('A1111/launch.py')
        self.args = args or ''
    def launch(self):
        if check(self.cwd) is False:
            run('git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git A1111', cwd=WORKSPACE)
        cf = check(self.file,isfile=True)
        if cf is False:
            print('Can`t Find launch.py [A1111]')
        elif cf is True:
            run(f'COMMANDLINE_ARGS="{self.args}" REQS_FILE="requirements.txt" python {self.file}', cwd=self.cwd)

class ComfyUi:
    def __init__(self,*, cwd=None, file=None, args=None):
        self.cwd = cwd or get_path('ComfyUI')
        self.file = file or get_path('ComfyUI/main.py')
        self.args = args or ''
    def launch(self):
        if check(self.cwd) is False:
            run('git clone https://github.com/comfyanonymous/ComfyUI.git ComfyUI', cwd=WORKSPACE)
        cf = check(self.file,isfile=True)
        if cf is False:
            print('Can`t Find main.py [ComfyUI]')
        elif cf is True:
            run('dpkg cloudflared-linux-amd64.deb', cwd=get_cwd(), quiet=True, msg='Install Cloudflared for LinuxAMD64')
            def cloudflare_tunnel(port):
                while True:
                    time.sleep(0.5)
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    result = sock.connect_ex(('127.0.0.1', port))
                    if result == 0:
                        break
                    sock.close()
                print("\nComfyUI finished loading, trying to launch cloudflared (if it gets stuck here cloudflared is having issues)\n")
                p = subprocess.Popen(["cloudflared", "tunnel", "--loglevel", "info", "--url", "http://127.0.0.1:{}".format(port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                for line in p.stderr:
                    l = line.decode()
                    if "trycloudflare.com " in l:
                        print("This is the URL to access ComfyUI:", l[l.find("http"):], end='')

            threading.Thread(target=cloudflare_tunnel, daemon=True, args=(8188,)).start()
            run(f'python {self.file} {self.args}', cwd=self.cwd)

class SDNext:
    def __init__(self,*, cwd=None, file=None, args=None):
        self.cwd = cwd or get_path('SDNext')
        self.file = file or get_path('SDNext/launch.py')
        self.args = args or ''
    def launch(self):
        if check(self.cwd) is False:
            run('git clone https://github.com/vladmandic/automatic.git SDNext', cwd=WORKSPACE)
        cf = check(self.file,isfile=True)
        if cf is False:
            print('Can`t Find launch.py [SDNext]')
        elif cf is True:
            run(f'COMMANDLINE_ARGS="{self.args}" python {self.file}', cwd=self.cwd)
