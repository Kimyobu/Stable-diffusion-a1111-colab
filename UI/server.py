import sys
import os.path as Path
import logging
from flask import Flask
from module.utils import get_path

port = int(sys.argv[1])
file = Path.realpath(__file__)
DIR = Path.dirname(file)

logging.basicConfig(filename=get_path('logs/server.log'), level=logging.DEBUG)
app = Flask('ManagerUI')

def read(path:str):
    f = open(path, 'r')
    d = f.read()
    f.close()
    return d

@app.get('/')
def home():
    page = read('./ui.html')
    return page


if __name__ == '__main__':
    app.run(port=port, debug=False)