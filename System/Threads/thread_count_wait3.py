"""
passed in mutex object shared by all threads instead of globals;
use with context manager statement for auto acquire/release;
sleep calls added to avoid busy loops and simulate real work
"""

import _thread as thread, time

stdoutmutex = thread.allocate_lock()
numthreads = 5
exitmutexes = [thread.allocate_lock() for i in range(numthreads)]

def counter(myId, count, mutex):
    for i in range(count):
        mutex.acquire()
        print('[%s] => %s' % (myId, i))
        mutex.release()
    exitmutexes[myId].acquire()

for i in range(numthreads):
    thread.start_new_thread(counter, (i, 100, exitmutexes[i]))
                            
while not all(mutex.locked() for mutex in exitmutexes): time.sleep(0.25)

print('Main thread exiting')