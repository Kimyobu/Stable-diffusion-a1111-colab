import subprocess
import sys
import os.path as Path

PATH = '/content/A1111'
req = Path.join(PATH,'requirements.txt')
file = Path.join(PATH,'launch.py')

def is_installed():
    return Path.isdir(PATH)

def App(args):
    return subprocess.Popen(f'COMMANDLINE_ARGS="{args}" {sys.executable} {file}', shell=True, cwd=PATH,stdout=subprocess.PIPE,stderr=subprocess.PIPE, universal_newlines=True)

