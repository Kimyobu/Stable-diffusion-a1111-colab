#@markdown #**Setup webUI**<br>
#@markdown > Clone Stable diffusion webui git repo<br>* caution if instant_replace = True will destroy and replace webUI folder<br>* คำเตือนเปิด instant_replace จะลบ folder webUI แล้วลงใหม่ข้อมูลหายหมด
instant_replace = False #@param {type: "boolean"}
#@markdown
install_extension = True #@param {type: "boolean"}
import time
import sys
import os
from google.colab import drive, output
!!apt-get -y install -qq aria2

env_name = 'project_path'
os.environ[env_name] = '/content/drive/MyDrive/kim-colab-project'
def mount():
    c = True
    p = '/content/drive'
    if os.path.exists(p):
        c = False
    if c :
        drive.mount(p, force_remount=True)

def pp(path = ''):
    mount()
    env_name = 'project_path'
    return os.environ[env_name] + path

def join(d:str, l: list[str], *a:str):
    for x in a:
        l.append(x)
    return d.join(l)

def rd(l:list):
    return [*set(l)]

def wait(t:float):
    time.sleep(t)


def git_clone(repo:list[str], path:str | None = None):
    if path:
        %cd {path}
    for x in repo:
        !git clone {x}
    %cd

def clear():
    output.clear()

def rm(path:str, arg = ''):
    if arg == '-r':
        os.removedirs(path)
    else:
        os.remove(path)

def dl(link:str, dir: str | None = None):
    link = f"\"{link}\""
    if dir: 
        !aria2c --console-log-level=error -c -x 16 -s 16 -k 1M {link} -d {dir}
    else:
        !aria2c --console-log-level=error -c -x 16 -s 16 -k 1M {link}

j = 'https://github.com/AUTOMATIC1111/stable-diffusion' + '-webui'
if instant_replace and os.path.exists(pp()):
  rm(pp(), '-r')

p = pp()
!git clone {j} {p}
if install_extension:
   !apt-get -y install -qq aria2
   dl('https://github.com/Kimyobu/Stable-diffusion-a1111-colab/raw/main/extensions.txt')
   #@markdown > Leave it default to install common extensions<br>ไม่ต้องเปลี่ยนถ้าจะลง extension ทั่วไป
   extension_list_file = '/content/extensions.txt' #@param {type: "string"}
   install = open(extension_list_file, 'r').read().split('\n')
   git_clone(install, pp('/extensions'))

os.environ['setup'] = 'True'
clear()
print('\033[38;5;82m' + 'Setup WebUI Complete')

#Cell 2
#@markdown #Model Installer
import os
if not os.environ.get('setup'):
    raise SystemExit('\033[31mRun SetUP WebUI FIRST!!\033[39m')
!apt-get -y install -qq aria2
model_type = 'ControlNet' #@param ["adetailer","deepdanbooru","karlo","sam","VAE-approx","Codeformer","ESRGAN","LDSR","Stable-diffusion","ControlNet","GFPGAN","Lora","SwinIR","deepbooru","hypernetworks","LyCORIS","VAE"]
model_path = ''
if model_type == 'ControlNet':
    model_path = pp('extensions/sd-webui-controlnet/models')
else :
    model_path = pp('/models') + model_type
model_url = 'https://civitai.com/api/download/models/11745' #@param {type:"string"}
!mkdir -p {model_path}
dl(model_url, model_path)

#Cell 3
#@markdown #**Launch WebUI**
import os
if not os.environ.get('setup'):
    raise SystemExit('\033[31mRun SetUP WebUI FIRST!!\033[39m')
p = pp()
%cd {p}
!pip install --upgrade fastapi
#!git stash
#!git pull origin master
#!git checkout b6af0a3809ea869fb180633f9affcae4b199ffcf
!apt install libcairo2-dev pkg-config python3-dev
!pip install svglib
!pip install pytorch-lightning==1.6.5
!pip install torchmetrics==0.11.0
!apt-get -y install -qq aria2
dl('https://raw.githubusercontent.com/Kimyobu/Stable-diffusion-a1111-colab/main/styles.csv')
clear()
# Web UI tunnel
!COMMANDLINE_ARGS="--share --no-half-vae --xformers --enable-insecure-extension- --theme dark --gradio-queue" REQS_FILE="requirements.txt" python launch.py