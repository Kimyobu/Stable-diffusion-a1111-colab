/**
 * @type {{name:string,defaultArgs:string,onclick:(this: HTMLElement, ev: MouseEvent) => void}[]}
 */
let app = [
    {
        name: 'ComfyUI',
        defaultArgs: '',
        onclick(ev) {
            alert('Start ComfyUI')
        }
    },
    {
        name: 'A1111',
        defaultArgs: '',
        onclick(ev) {
            
        }
    },
    {
        name: 'SDNext',
        defaultArgs: '',
        onclick(ev) {

        }
    }
]


window.onload = function () {
    console.log('Test')

    let main = document.querySelector('.main')
    app.forEach(a => {
        // สร้าง element div
        let node = document.createElement('div');
        node.className = 'row';

        // เพิ่มข้อความ 'A1111' เป็น text node ใน div
        let title = document.createTextNode(a.name);
        node.appendChild(title);

        // เพิ่ม input checkbox และ label 'Installed'
        let installed = document.createElement('input');
        installed.type = 'checkbox';
        let labelInstalled = document.createElement('label');
        labelInstalled.textContent = 'Installed';
        node.appendChild(installed);
        node.appendChild(labelInstalled);

        // เพิ่ม input checkbox และ label 'Use Google Drive'
        let use_g_drive = document.createElement('input');
        use_g_drive.type = 'checkbox';
        let labelGoogleDrive = document.createElement('label');
        labelGoogleDrive.textContent = 'Use Google Drive';
        node.appendChild(use_g_drive);
        node.appendChild(labelGoogleDrive);

        // สร้าง div ใน div และเพิ่มข้อความและ input text ใน div ใหม่
        let commandLineDiv = document.createElement('div');
        commandLineDiv.style.display = 'inline-block';
        let commandLineText = document.createTextNode(' | CommandLineArgs:');
        let inputCommandLine = document.createElement('input');
        inputCommandLine.type = 'text';
        inputCommandLine.className = 'dynamic-input';
        inputCommandLine.value = a.defaultArgs
        inputCommandLine.oninput = function () {
            resizeInput(inputCommandLine);
        };
        commandLineDiv.appendChild(commandLineText);
        commandLineDiv.appendChild(inputCommandLine);
        node.appendChild(commandLineDiv);

        // เพิ่ม button 'Launch'
        let launchButton = document.createElement('button');
        launchButton.className = 'la';
        launchButton.textContent = 'Launch';
        launchButton.addEventListener('click', a.onclick)
        node.appendChild(launchButton);

        main.appendChild(node)

    })


    document.querySelectorAll('#readonly').forEach((e) => {
        e.addEventListener('click', (ev) => {
            ev.preventDefault()
        })
    })
}
