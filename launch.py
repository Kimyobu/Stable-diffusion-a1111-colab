import gradio as gr
import os
import subprocess
import sys

def run(cmd:str):
    return subprocess.run(cmd.split(' '))

def py(cmd:str):
    return run(f'{sys.executable} {cmd}')

def op(choices=[],value=[]):
    return gr.CheckboxGroup(['Use Google Drive']+choices,value=[True]+value)

def label(title):
    gr.Text(lines=0,max_lines=0,interactive=False,show_label=False,value=title)

def la():
    return gr.Button('Launch')

def arg(default):
    return gr.Textbox(default,lines=1,max_lines=1,placeholder='Place your commandline args here...')

def a1111_click(args,option):
    py('/content/A1111/launch.py')
    return 'Started A1111'

with gr.Blocks() as ui:
    status = gr.Text(label='Status',interactive=False)
    with gr.Tab('WebUi Launcher'):
        with gr.Row():
            label('ComfyUi')
            comfy_dr = op()
            comfy = la()
        with gr.Row():
            label('A1111')
            a1111_args = arg('--share --no-half-vae --xformers --enable-insecure-extension- --theme dark')
            a1111_d = op()
            a1111 = la()
        with gr.Row():
            label('SDNext')
            sdnext_drive = op()
            sdnext = la()
    with gr.Tab('Github'):
        ui
    with gr.Tab('Models Downloader'):
        ui
    with gr.Tab('File Manager'):
        ui

    a1111.click(fn=a1111_click,inputs=[a1111_args,a1111_d],outputs=[status])

def start():
    print('StartUP!!!')

ui.startup_events = start

ui.launch(debug=True,share=True,show_error=True)
