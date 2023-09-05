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
        self.cwd = cwd or get_path('A1111')
        self.file = file or get_path('A1111/launch.py')
        self.args = args or ''
    def launch(self):
        if check(self.cwd) is False:
            run('git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git', cwd=WORKSPACE)
        elif check(self.cwd) is True:
            cf = check(self.file,isfile=True)
            if cf is False:
                print('Can`t Find launch.py [A1111]')
            elif cf is True:
                return py('launch.py', cwd=self.cwd)


