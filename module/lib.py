import subprocess
import sys

def run(cmd):
    return subprocess.run(cmd)

def git_clone(repo,*args:str):
    return run(['git','clone',repo]+list(args))

def py(cmd:str):
    return run([sys.executable]+cmd.split(' '))

