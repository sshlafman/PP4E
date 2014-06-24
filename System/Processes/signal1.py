"""
catch signals in Python; pass signal number N as a command-line arg,
user a "kill -N pid" shell command to send this process a signal; most
signal handlers restored by Python after caught (see network scripting
chanpter for SIGCHLD details); on Windows, signal module is available,
but it defines only a few signal types there, and os.kill is missing;
"""

import sys, signal, time

def now(): return time.ctime(time.time())  # current time string

def onSignal(signum, stackframe):
    print('Got signal', signum, 'at', now())
    
signum = int(sys.argv[1])
signal.signal(signum, onSignal)    # install signal handler
while True: signal.pause()         # wait for signals (or: pass)