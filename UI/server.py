import sys
import os.path as Path
import os
import threading
import json
import re
from flask import Flask, request, jsonify, redirect
from flask_socketio import SocketIO, emit

from module import A1111

def get_file(*path:str):
    return Path.join(Path.dirname(__file__), *path)

if not Path.isdir(get_file('.temp')):
    os.mkdir(get_file('.temp'))

def get_temp(mode='w'):
    return open(get_file('.temp', 'temp.json'), mode)

temp = get_temp()
temp.write('{}')
temp.close()

app = Flask(__name__)
socketio = SocketIO(app, async_mode='gevent')
args = sys.argv[1:]
port = int(args[0])

#Home Page
@app.get('/')
def home():
    page = open(get_file('ui.html'))
    return page.read(), 200

@socketio.on('connect')
def handle_connect():
    print('Client connected')  # แสดงข้อความเมื่อมีการเชื่อมต่อ

#Listen for launch button click
@app.post('/la')
def la():
    data_json = request.get_json()
    data = jsonify(data_json)

    out = None
    temp = get_temp('r')
    f = json.loads(temp.read())

    name = data_json['name']
    lock = data_json['lock']
    rename = data_json['rename']

    f['la'] = data_json.get('la') or {}
    f['la'][name] = {
            'name': rename,
            'lock': lock
        }
    temp = get_temp()
    temp.write(json.dumps(f, indent=2))
    temp.close()
    name = data_json['name']
    la_args = data_json['args']
    if name == 'ComfyUI':
        pass
    elif name == 'A1111':
        p = A1111.App(la_args)
        def a1111():
            for line in p.stdout:
                emit('output', line)

        thread = threading.Thread(target=a1111, daemon=True)
        thread.start()
    elif name == 'SDNext':
        pass

    return data, 201

#Get listen for get config
@app.get('/get-config')
def get_json():
    file = open(get_file('config.json'),'r')
    data = file.read()
    file.close()
    data_dict = json.loads(data)
    return jsonify(data_dict), 200

#Get listen for get temp data
@app.route('/temp-data', methods=['GET', 'POST'])
def temp_data():
    if request.method == 'GET':
        file = open(get_file('.temp', 'temp.json'),'r')
        data = file.read()
        file.close()
        return jsonify(json.loads(data)), 200
    elif request.method == 'POST':
        return 'None', 201

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

if __name__ == '__main__':
    socketio.run(app,port=port,debug=False)