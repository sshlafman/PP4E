"""
fork child process to watch exit status with os.wait; fork works on Unix
and Cygwin but not standard Windows Python 3.1; note: spawned threads share
globals, but each forked process has itsown copy of them (forks share file
descriptors)--exitstat is always the same here but will vary if for threads;
"""

import os
exitstat = 0

def child():
    global exitstat
    exitstat += 1
    print('Hello from child', os.getpid(), exitstat)
    os._exit(exitstat)
    print('never reached')
    
def parent():
    while True:
        newpid = os.fork()
        if newpid == 0:
            child()
        else:
            pid, status = os.wait()
            print('Parent got', pid, status, (status >> 8))
            if input() == 'q':  break

if __name__ == '__main__': parent()
        