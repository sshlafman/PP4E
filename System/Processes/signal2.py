"""
set and catch alarm timeout signals in Python; time.sleep doesn't play
well with alarm (or signal in general in Linux PC), so we call
signal.pause here to do nothing until a signal is received;
"""

import signal, time

def now(): return time.asctime()

def onSignal(signum, stackframe):
    print('Got signal', signum, 'at', now())
    
while True:
    print('Setting at', now())
    signal.signal(signal.SIGALRM, onSignal)
    signal.alarm(5)                            # do signal in 5 seconds
    signal.pause()