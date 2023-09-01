import subprocess
import sys
import threading
import time
import socket
import os.path as Path

def iframe_thread(port):
  while True:
      time.sleep(0.5)
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      result = sock.connect_ex(('127.0.0.1', port))
      if result == 0:
        break
      sock.close()
  p = subprocess.Popen(["cloudflared", "tunnel", "--loglevel", "info", "--url", "http://127.0.0.1:{}".format(port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  for line in p.stderr:
    l = line.decode()
    if "trycloudflare.com " in l:
      print("This is the URL to access ManagerUI:", l[l.find("http"):], end='')
    #print(l, end='')

port = int(sys.argv[1])

threading.Thread(target=iframe_thread, daemon=True,args=(port,)).start()

try:
    subprocess.run([sys.executable, Path.join(Path.dirname(__file__), 'server.py'), str(port)])
except KeyboardInterrupt:
  print('Closing Server...')