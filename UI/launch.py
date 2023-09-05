import subprocess
import sys
import time
import socket
import threading
import logging
import os.path as Path
from module.utils import run, get_path

logging.basicConfig(filename=get_path('logs/launch.log'), level=logging.DEBUG)

port = int(sys.argv[1])
file = Path.realpath(__file__)
DIR = Path.dirname(file)

print('Install Cloudflared for LinuxAMD64')
run('dpkg cloudflared-linux-amd64.deb', cwd=DIR, quiet=True)
print('Starting Server...')

def iframe_thread(port):
  return subprocess.run(f'python server.py {port}' ,shell=True, cwd=DIR)

threading.Thread(target=iframe_thread, daemon=True,args=(port,)).start()

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