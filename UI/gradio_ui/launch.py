import subprocess
import sys
import os
from utils import is_installed, run_pip, py

args = sys.argv[1:]
PORT = int(args[0])

run_pip('gradio==3.41.2')

try:
    print('Starting Server...')
    py(f'./server.py {PORT}')
except KeyboardInterrupt:
    print('Stopped Server...')