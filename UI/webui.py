import argparse
from module.colab import ComfyUi, A1111, SDNext
from module.utils import mount_drive

parser = argparse.ArgumentParser(description="")

parser.add_argument("--app", type=str, help="Name of app to be launch")
parser.add_argument("--cwd", type=str, help="Path Working Directory of App")
parser.add_argument("--file", type=str, help="Path File of launching App")
parser.add_argument("--args", type=str, help="Argument to be use for launching App")
parser.add_argument("--use_google_drive", action='store_true', help="If set use google drive storage to locate program location")

args = parser.parse_args()

App = args.app
Cwd = args.cwd
File = args.file
Args = args.args
Use_drive = args.use_google_drive

if Use_drive is True:
    mount_drive()

if App is not None:
    print(f'Finding {App}...')
    if App == 'ComfyUi':
        ComfyUi(cwd=Cwd, file=File, args=Args, use_drive=Use_drive).launch()
    elif App == 'A1111':
        A1111(cwd=Cwd, file=File, args=Args, use_drive=Use_drive).launch()
    elif App == 'SDNext':
        SDNext(cwd=Cwd, file=File, args=Args, use_drive=Use_drive).launch()
