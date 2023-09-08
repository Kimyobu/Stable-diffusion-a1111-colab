import importlib
import subprocess
import sys
import os
import os.path as Path
from importlib.metadata import version
from google.colab import drive

Dir = Path.dirname(Path.realpath(__file__))
WORKSPACE = Path.dirname(Dir)

def mount_drive(path='/content/drive'):
    if Path.isdir(path) is False:
        print('Mounting google drive...')
        drive.mount(path, force_remount=True)

def is_installed(name:str,pkg_version:str or None=None):
    out = False
    package = importlib.util.find_spec(name)
    if package is not None:
        out = True
        if pkg_version is not None:
            if version(package.name) != pkg_version:
                out = False
    
    return out

def run(cmd:str,*, cwd=Dir, quiet=False, msg=None):
    stdout = subprocess.DEVNULL if quiet == True else None
    stderr = subprocess.STDOUT if quiet == True else None
    if msg:
        print(msg)
    return subprocess.run(args=cmd, cwd=cwd, shell=True, stdout=stdout, stderr=stderr)

def py(command, *, cwd=Dir, quiet=False):
    return run(f'{sys.executable} {command}', cwd=cwd, quiet=quiet)

def run_pip(install_syntex:str):
    parse = install_syntex.split('==')
    name = parse[0]
    ver = parse[1] if len(parse) > 1 else None
    if not is_installed(name,ver):
        print(f'Install {install_syntex}')
        py(f'-m pip install {install_syntex}', quiet=True)

def get_path(path):
    return Path.join(WORKSPACE, path)

def get_cwd():
    return WORKSPACE