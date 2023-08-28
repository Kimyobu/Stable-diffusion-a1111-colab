import os
import threading
from google.colab import drive,output
from .lib import py

class App:
    def __init__(self,*, use_drive=False, args='--share --no-half-vae --xformers --enable-insecure-extension- --theme dark'):
        WORKSPACE = '/content/A1111'
        if use_drive:
            if not os.path.isdir('/content/drive'):
                print('Mounting Drive...')
                drive.mount('/content/drive', force_remount=True)
            WORKSPACE = '/content/drive/MyDrive/'
        def run():
            return py(f'{WORKSPACE}/launch.py')
        threading.Thread(target=run)