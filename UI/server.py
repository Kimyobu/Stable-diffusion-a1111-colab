from flask import Flask, request, jsonify
import sys
import subprocess
import json
import os.path as Path

from module import A1111

app = Flask(__name__)
args = sys.argv[1:]
port = int(args[0])

@app.get("/")
def home():
    page = open(Path.join(Path.dirname(__file__), 'ui.html'))
    return page.read(), 200

@app.post("/la")
def la():
    data_json = request.get_json()
    data = jsonify(data_json)

    name = data_json['name']
    la_args = data_json['args']
    if name == 'ComfyUI':
        pass
    elif name == 'A1111':
        A1111.App(la_args)
    elif name == 'SDNext':
        pass

    return data, 201

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

if __name__ == '__main__':
    app.run(port=port,debug=False)