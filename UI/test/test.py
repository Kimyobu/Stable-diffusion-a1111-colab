import subprocess
import threading
import time

def run():
    p = subprocess.Popen(['python', './run.py'])
    stdout,stderr = p.communicate()
    print(stdout)

t = threading.Thread(target=run,daemon=True)
t.start()


while True:
    time.sleep(.1)