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

def is_installed(name: str, pkg_version: str or None = None, operator: str = '=='):
    out = False
    try:
        package = importlib.util.find_spec(name)
        if package is not None:
            out = True
            if pkg_version is not None:
                ver = version(package.name)
                if operator == '==':
                    out = (ver == pkg_version)
                elif operator == '>=':
                    out = (ver >= pkg_version)
                elif operator == '<=':
                    out = (ver <= pkg_version)
                elif operator == '<':
                    out = (ver < pkg_version)
                elif operator == '>':
                    out = (ver > pkg_version)
                elif operator == '!=':
                    out = (ver != pkg_version)
                elif operator == '~=':
                    out = (pkg_version in package.requires)
    except ModuleNotFoundError:
        pass
    return out

def run(cmd:str,*, cwd=Dir, quiet=False, msg=None):
    stdout = subprocess.DEVNULL if quiet == True else None
    stderr = subprocess.STDOUT if quiet == True else None
    if msg is not None:
        print(msg)
    if Path.isdir(cwd) is False:
        os.makedirs(cwd, exist_ok=True)
    return subprocess.run(args=cmd, cwd=cwd, shell=True, stdout=stdout, stderr=stderr)

def py(command, *, cwd=Dir, quiet=False, msg=None):
    return run(f'{sys.executable} {command}', cwd=cwd, quiet=quiet, msg=msg)

def run_pip(install_syntax: str):
    operators = ['<', '>', '==', '>=', '<=' , '!=']
    found = []

    for op in operators:
        if op in install_syntax:
            found.append(op)

    operator = found[-1] if len(found) > 0 else '=='

    if operator is not None:
        package_info = install_syntax.split(operator)
        name = package_info[0].strip()
        version = package_info[1].strip() if len(package_info) > 1 else None

        if is_installed(name, version, operator) is False:
            print(f'Install {install_syntax}')
            py(f'-m pip install {install_syntax}', quiet=True)

def get_path(path):
    return Path.join(WORKSPACE, path)

def get_cwd():
    return WORKSPACE