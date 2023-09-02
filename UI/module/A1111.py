import threading
import subprocess
import sys
import os.path as Path

PATH = '/content/A1111'
req = Path.join(PATH,'requirements.txt')
file = Path.join(PATH,'launch.py')

def la(args):
    return subprocess.run(f'COMMANDLINE_ARGS="{args}" {sys.executable} {file}', shell=True, cwd=PATH)

def App(args:str):
    threading.Thread(target=la,daemon=True,args=[args,]).start()
