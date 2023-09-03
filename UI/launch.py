import subprocess
import sys
import threading
import time
import socket
import os.path as Path
from module.utils import run_pip

subprocess.run('dpkg -i /content/kim-colab-project/UI/cloudflared-linux-amd64.deb', shell=True, stdout=subprocess.DEVNULL)

PATH = Path.realpath(__file__)
DIR = Path.dirname(PATH)

requirements = open(Path.join(DIR, 'requirements.txt'))
reqs = requirements.read()
requirements.close()
for r in reqs.split('\n'):
   run_pip(r)

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

port = int(sys.argv[1])

threading.Thread(target=iframe_thread, daemon=True,args=(port,)).start()

try:
    subprocess.run([sys.executable, Path.join(Path.dirname(__file__), 'server.py'), str(port)], stdout=subprocess.PIPE, universal_newlines=True)
except KeyboardInterrupt:
  print('Closing Server...')