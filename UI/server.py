import sys
import os.path as Path
import os
import threading
import json
import re
import logging
from flask import Flask, request, jsonify, redirect
from flask_socketio import SocketIO

from module import A1111

def get_file(*path:str):
    return Path.join(Path.dirname(__file__), *path)

if not Path.isdir(get_file('.temp')):
    os.mkdir(get_file('.temp'))

def get_temp(mode='w',file='temp.json'):
    return open(get_file('.temp', file), mode)

def parse_url(text:str):
    url_pattern = r'https?://\S+'
    return re.findall(url_pattern, text)

temp = get_temp()
temp.write('{}')
temp.close()
log = get_temp(file='log.txt')
log.write('')
log.close()



app = Flask(__name__)
socketio = SocketIO(app, async_mode='gevent')
args = sys.argv[1:]
port = int(args[0])

def info(msg:str):
    return socketio.server.logger.info(msg)

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

    name = data_json['name']
    lock = data_json['lock']
    rename = data_json['rename']

    out = None
    la_args = data_json['args']
    info(f'Name: {name}')
    try:
        p = None
        if name == 'ComfyUI':
            pass
        elif name == 'A1111':
            p = A1111.App(la_args)
        elif name == 'SDNext':
            pass
        if p is not None:
            def run():
                stdout,stderr = p.communicate()
                # text = stdout.decode()
                
                log = get_temp(mode='a',file='log.txt')
                log.write(stdout)
                socketio.emit('output',{'body':stdout})
                p.wait()
                log.close()
            thread = threading.Thread(target=run, daemon=True)
            thread.start()
            temp = get_temp('r')
            f = json.loads(temp.read())

            f['la'] = data_json.get('la') or {}
            f['la'][name] = {
                    'name': rename,
                    'lock': lock
                }
            temp = get_temp()
            temp.write(json.dumps(f, indent=2))
            temp.close()
            name = data_json['name']
    except Exception as e:
        data = f"Error:{type(e).__name__}\n{str(e)}\n{e.args}"
        print(data,end='')
        log = get_temp(mode='a',file='log.txt')
        log.write(data)
        log.close()
        socketio.emit('output',{'body':data})

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
        file = get_temp('r')
        data = json.loads(file.read())
        file.close()
        log = get_temp('r', 'log.txt')
        log_data = log.read()
        log.close()

        data['log'] = log_data

        return jsonify(data), 200
    elif request.method == 'POST':
        data = request.get_json()
        if data.get('name') == 'reset-log':
            log = get_temp('w', 'log.txt')
            log.write('')
            log.close()
            return 'Reset-log!!', 201
        return 'None', 201

if __name__ == '__main__':
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    socketio.run(app,port=port,debug=False)