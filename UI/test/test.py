from flask import Flask
import logging
import time
import socket
import subprocess
import sys
import threading
 
app = Flask(__name__)
 
logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
 
@app.route('/blogs')
def blog():
    app.logger.info('Info level log')
    app.logger.warning('Warning level log')
    return f"Welcome to the Blog"

port = int(sys.argv[1])

def iframe_thread(port):
  while True:
      time.sleep(0.5)
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      result = sock.connect_ex(('127.0.0.1', port))
      if result == 0:
        print(f'Starting Local Server as http://127.0.0.1:{port}')
        break
      sock.close()
  p = subprocess.Popen(["cloudflared", "tunnel", "--loglevel", "info", "--url", f"http://127.0.0.1:{port}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  for line in p.stderr:
    l = line.decode()
    if "trycloudflare.com " in l:
      print("Starting Public Server as", l[l.find("http"):], end='')
    #print(l, end='')

def test():
   p = subprocess.Popen('python run.py', shell=True)
   stdout,stderr = p.communicate()
   app.logger.info(stdout,stderr)

threading.Thread(target=test,daemon=True).start()
threading.Thread(target=iframe_thread, daemon=True,args=(port,)).start()
app.run(host='localhost', debug=True, port=port)