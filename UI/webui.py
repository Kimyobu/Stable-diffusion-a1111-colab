import argparse
from module.colab import A1111

parser = argparse.ArgumentParser(description="")

parser.add_argument("--app", type=str, help="Name of app to be launch")
parser.add_argument("--cwd", type=str, help="Path Working Directory of App")
parser.add_argument("--file", type=str, help="Path File of launching App")
parser.add_argument("--args", type=str, help="Argument to be use for launching App")

args = parser.parse_args()

App = args.app
Cwd = args.cwd
File = args.file
Args = args.args

if App is not None:
    print(f'Finding {App}...')
    if App == 'ComfyUi':
        pass
    elif App == 'A1111':
        A1111(cwd=Cwd, file=File, args=Args)

