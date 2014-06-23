"""
spawn a child process/program, connect my stdin/stdout to child process's
stdout/stdin--my reads and writes map to output and input streams of the
spawned program; much like tying together streams with subprocess module;
"""

import os, sys

def spawn(prog, *args):
    stdinFd  = sys.stdin.fileno()
    stdoutFd = sys.stdout.fileno()
    
    parentStdin, childStdout = os.pipe()
    childStdin, parentStdout = os.pipe()
    pid = os.fork()
    if pid:
        os.close(childStdout)
        os.close(childStdin)
        os.dup2(parentStdin, stdinFd)     # my sys.stdin copy = pipe1[0]
        os.dup2(parentStdout, stdoutFd)   # my sys.stdout copy = pipe2[1]
    else:
        os.close(parentStdin)
        os.close(parentStdout)
        os.dup2(childStdin, stdinFd)      # my sys.stdin copy = pipe2[0]
        os.dup2(childStdout, stdoutFd)    # my sys.stdin copy = pipe1[1]
        args = (prog,) + args
        os.execvp(prog, args)             # new program in this process
        assert False, 'execvp failed!'    # os.exec call never returns here
        
if __name__ == '__main__':
    mypid = os.getpid()
    spawn('python', 'pipes_testchild.py', 'spam')
    
    print('Hello 1 from parent', mypid)
    sys.stdout.flush()                     # subvert stdio buffering
    reply = input()
    sys.stderr.write('Parent got: "%s"\n' % reply)
    
    print('Hello 2 from parent', mypid)
    sys.stdout.flush()
    reply = sys.stdin.readline()
    sys.stderr.write('Parent got: "%s"\n' % reply[:-1])