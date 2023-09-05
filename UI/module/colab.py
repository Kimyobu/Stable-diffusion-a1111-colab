import subprocess
import os.path as Path
import os
from .utils import run,py

WORKSPACE = '/content'

def get_path(path:str):
    return Path.join(WORKSPACE, path)

def check(path:str,isfile=False):
    return Path.isfile(path) if isfile is True else Path.isdir(path)

class A1111:
    def __init__(self,*, cwd=None, file=None, args=None):
        self.cwd = cwd or get_path('ComfyUI')
        self.file = file or get_path('ComfyUI/launch.py')
        self.args = args or ''
    def launch(self):
        if check(self.cwd) is False:
            run('git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git', cwd=WORKSPACE)
        elif check(self.cwd) is True:
            cf = check(self.file,isfile=True)
            if cf is False:
                print('Can`t Find launch.py [A1111]')
            elif cf is True:
                return run(f'COMMANDLINE_ARGS="{self.args}" REQS_FILE="requirements.txt" python {self.file}', cwd=self.cwd)

class ComfyUi:
    def __init__(self,*, cwd=None, file=None, args=None):
        self.cwd = cwd or get_path('ComfyUI')
        self.file = file or get_path('ComfyUI/main.py')
        self.args = args or ''
    def launch(self):
        if check(self.cwd) is False:
            run('git clone https://github.com/comfyanonymous/ComfyUI.git', cwd=WORKSPACE)
        elif check(self.cwd) is True:
            cf = check(self.file,isfile=True)
            if cf is False:
                print('Can`t Find main.py [ComfyUI]')
            elif cf is True:
                return run(f'python {self.file} {self.args}', cwd=self.cwd)

class SDNext:
    def __init__(self,*, cwd=None, file=None, args=None):
        self.cwd = cwd or get_path('SDNext')
        self.file = file or get_path('SDNext/launch.py')
        self.args = args or ''
    def launch(self):
        if check(self.cwd) is False:
            run('git clone https://github.com/vladmandic/automatic.git', cwd=WORKSPACE)
        elif check(self.cwd) is True:
            cf = check(self.file,isfile=True)
            if cf is False:
                print('Can`t Find launch.py [SDNext]')
            elif cf is True:
                return run(f'COMMANDLINE_ARGS="{self.args}" python {self.file}', cwd=self.cwd)
