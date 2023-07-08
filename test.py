import sys
import os

def leave():
    raise StopIteration()


print('Start')
leave()
print('Not leave')