import subprocess
import os.path as Path
import os
import time
import threading
import socket
from .utils import run, py, get_cwd, run_pip

Config = {
    "WS": "/content",
    "DRIVE": "/content/drive/MyDrive/kim-colab-project"
}

WORKSPACE = Config.get("WS")
DRIVE = Config.get("DRIVE")
PROJECT = Path.dirname(get_cwd())

def get_path(path:str=None):
    return Path.join(Config.get("WS"), path) if path is not None else Config.get("WS")

def check(path:str,isfile=False):
    return Path.isfile(path) if isfile is True else Path.isdir(path)

def git_clone_from_file(file, cwd):
    op = open(file, 'r')
    r = op.read()
    op.close()
    for x in r.split('\n'):
        name = Path.splitext(Path.basename(x))[0]
        if check(Path.join(cwd, name)) is False:
            run(f'git clone {x} {name}', cwd=cwd, msg=f'Install extension {name}')

class A1111:
    def __init__(self,*, cwd=None, file=None, args=None, use_drive=False):
        if use_drive is True:
            Config['WS'] = DRIVE
        self.cwd = cwd or get_path('A1111')
        self.file = file or get_path('A1111/launch.py')
        self.args = args or ''
    def launch(self):
        if check(self.cwd) is False:
            run('git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git A1111', cwd=Path.dirname(self.cwd))
        cf = check(self.file,isfile=True)
        if cf is False:
            print('Can`t Find launch.py [A1111]')
        elif cf is True:
            run_pip('pytorch-lightning==1.6.5')
            run_pip('torchmetrics==0.11.0')
            run_pip('pydantic==1.10.5')
            run_pip('pillow==9.5.0')
            run_pip('open-clip-torch==2.20.0')
            git_clone_from_file(Path.join(PROJECT, 'SD/extensions.txt'), Path.join(self.cwd, 'extensions'))

            #CodeFormer Pack Fix
            codeformer = get_path('A1111/repositories/CodeFormer')
            if check(codeformer) is True:
                run('git checkout -f c5b4593074ba6214284d6acd5f1719b6c5d739af', cwd=codeformer)

            run(f'COMMANDLINE_ARGS="{self.args}" REQS_FILE="requirements.txt" python {self.file}', cwd=self.cwd)

class ComfyUi:
    def __init__(self,*, cwd=None, file=None, args=None, use_drive=False):
        if use_drive is True:
            Config['WS'] = DRIVE
        self.cwd = cwd or get_path('ComfyUI')
        self.file = file or get_path('ComfyUI/main.py')
        self.args = args or ''
    def launch(self):
        if check(self.cwd) is False:
            run('git clone https://github.com/comfyanonymous/ComfyUI.git ComfyUI', Path.dirname(self.cwd))
        cf = check(self.file,isfile=True)
        if cf is False:
            print('Can`t Find main.py [ComfyUI]')
        elif cf is True:
            run('dpkg -i cloudflared-linux-amd64.deb', cwd=get_cwd(), quiet=True, msg='Install Cloudflared for LinuxAMD64')
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
    def __init__(self,*, cwd=None, file=None, args=None, use_drive=False):
        if use_drive is True:
            Config['WS'] = DRIVE
        self.cwd = cwd or get_path('SDNext')
        self.file = file or get_path('SDNext/launch.py')
        self.args = args or ''
    def launch(self):
        if check(self.cwd) is False:
            run('git clone https://github.com/vladmandic/automatic.git SDNext', Path.dirname(self.cwd))
        cf = check(self.file,isfile=True)
        if cf is False:
            print('Can`t Find launch.py [SDNext]')
        elif cf is True:
            run(f'COMMANDLINE_ARGS="{self.args}" python {self.file}', cwd=self.cwd)
