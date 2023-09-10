import argparse
from module.colab import ComfyUi, A1111, SDNext
from module.utils import mount_drive

parser = argparse.ArgumentParser(description="")

parser.add_argument("--app", type=str, help="Name of app to be launch")
parser.add_argument("--cwd", type=str, help="Path Working Directory of App")
parser.add_argument("--file", type=str, help="Path File of launching App")
parser.add_argument("--args", type=str, help="Argument to be use for launching App")
parser.add_argument("--use_google_drive", type=bool, help="If set will use google drive storage to locate program location")
parser.add_argument("--install_extensions", type=bool, help="If set will install all recommender extensions by Kimyobu")
parser.add_argument("--update", type=bool, help="If set will update selected app ui")
parser.add_argument("--update_exts", type=bool, help="If set will update all extensions/custom_nodes")
parser.add_argument("--force_update", type=bool, help="If set will instant replace a change (exclude none change from release)")
parser.add_argument("--install_req", type=bool, help="If set will installing requirement dependencies")

args = parser.parse_args()

App = args.app
Cwd = args.cwd
File = args.file
Args = args.args
Use_drive = args.use_google_drive
Install_exts = args.install_extensions
Update = args.update
Update_exts = args.update_exts
Force_update = args.force_update
Install_req = args.install_req

if Use_drive is True:
    mount_drive()

if App is not None:
    print(f'Finding {App}...')
    if App == 'ComfyUi':
        ComfyUi(cwd=Cwd, file=File, args=Args, use_drive=Use_drive, install_exts=Install_exts, update=Update, update_exts=Update_exts, force_update=Force_update, install_req=Install_req).launch()
    elif App == 'A1111':
        A1111(cwd=Cwd, file=File, args=Args, use_drive=Use_drive, install_exts=Install_exts, update=Update, update_exts=Update_exts, force_update=Force_update, install_req=Install_req).launch()
    elif App == 'SDNext':
        SDNext(cwd=Cwd, file=File, args=Args, use_drive=Use_drive, install_exts=Install_exts, update=Update, update_exts=Update_exts, force_update=Force_update, install_req=Install_req).launch()
