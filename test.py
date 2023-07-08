def join(d: str, l: list[str], *a:str):
    for x in a:
        l.append(x)
    return d.join(l)

# l = 'sky\nkim\nyou\nbun'
# s = l.split('\n')
# print(join('\n', s, 'new'))
def check():
    import os
    if not os.environ['setup']:
        raise SystemExit('\033[31mRun SetUP WebUI FIRST!!\033[39m')


import os
if not os.environ.get('setup'):
    raise UserWarning('\033[31mRun SetUP WebUI FIRST!!\033[39m')
    
print('\033[31mtest\033[39m')