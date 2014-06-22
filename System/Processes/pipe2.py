# same as pipe1.py, but wrap pipe input in stdio file object
# to read by line, and closed unused pipe fds in both processes

import os, time

def child(pipeout):
    zzz = 0
    while True:
        time.sleep(zzz)
        msg = ('Spam %03d\n' % zzz).encode()
        os.write(pipeout, msg)
        zzz = (zzz+1) % 5
        
def parent():
    pipein, pipeout = os.pipe()
    if os.fork() == 0:
        os.close(pipein)
        child(pipeout)
    else:
        os.close(pipeout)
        pipein = os.fdopen(pipein)
        while True:
            line = pipein.readline()[:-1]
            print('Parent %d got [%s] at %s' % (os.getpid(), line, time.time()))

parent()