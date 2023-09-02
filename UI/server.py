import sys
import os.path as Path
import os
import json
from flask import Flask, request, jsonify

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
args = sys.argv[1:]
port = int(args[0])

#Home Page
@app.get('/')
def home():
    page = open(get_file('ui.html'))
    return page.read(), 200

#Listen for launch button click
@app.post('/la')
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

#Get listen for get config
@app.get('/get-config')
def get_json():
    file = open(get_file('config.json'),'r')
    data = file.read()
    file.close()
    return jsonify(json.loads(data)), 200

#Get listen for get temp data
@app.route('/temp-data', methods=['GET', 'POST'])
def temp_data():
    if request.method == 'GET':
        file = open(get_file('.temp', 'temp.json'),'r')
        data = file.read()
        file.close()
        return jsonify(json.loads(data)), 200
    elif request.method == 'POST':
        req = request.get_json()
        temp = get_temp('r')
        data = json.loads(temp.read())

        name = req['name']
        lock = req['lock']
        rename = req['rename']

        data['la'] = data.get('la') or {}
        data['la'][name] = {
                'name': rename,
                'lock': lock
            }
        temp = get_temp()
        temp.write(json.dumps(data, indent=2))
        temp.close()
        return 'Saved', 201

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

if __name__ == '__main__':
    app.run(port=port,debug=False)