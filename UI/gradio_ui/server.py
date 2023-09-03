import gradio as gr
import sys
import os.path as Path
from UI.module.utils import py

args = sys.argv[1:]
PORT = int(args[0])

a1111_path = '/content/A1111'
a1111_file = Path.join(a1111_path, 'launch.py')

def a1111_run():
    py(a1111_file, cwd=a1111_path)

with gr.Blocks() as ui:
    with gr.Tab('Launcher'):
        with gr.Row():
            gr.Markdown('A1111')
            a1111 = gr.Button('Launch')
            a1111.click(fn=a1111_run)



ui.launch(server_port=PORT,share=True,show_api=True,show_error=True,show_tips=True)