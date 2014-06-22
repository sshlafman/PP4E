import os, time

def child(pipeout):
    zzz = 0
    while True:
        time.sleep(zzz)
        msg = ('Spam %03d' % zzz).encode()  # pipes are binary bytes
        os.write(pipeout, msg)
        zzz = (zzz+1) % 5
        
def parent():
    pipein, pipeout = os.pipe()
    if os.fork() == 0:
        child(pipeout)
    else:
        while True:
            line = os.read(pipein, 32)  # blocks until data sent
            print('Parent %d got [%s] at %s' % (os.getpid(), line, time.time()))
                  
parent()