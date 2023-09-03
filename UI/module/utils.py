import importlib
import subprocess
import sys
import os
import os.path as Path
from importlib.metadata import version

Dir = Path.dirname(Path.realpath(__file__))

def is_installed(name:str,pkg_version:str or None=None):
    out = False
    package = importlib.util.find_spec(name)
    if package is not None:
        out = True
        if pkg_version:
            if version(package.name) != pkg_version:
                out = False
    
    return out

def run(cmd:str,*, cwd=Dir, quiet=False):
    stdout = subprocess.DEVNULL if quiet == True else None
    stderr = subprocess.STDOUT if quiet == True else None
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
