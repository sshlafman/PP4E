"""
thread class instances with state and run() for thread's action;
uses higher-level Java-like threading module object join method (not
mutexes or shared global vars) to know when threads are done in main
parent thread; see library manual for more details on threading; 
"""

import threading

class Mythread(threading.Thread):
    def __init__(self, myId, count, mutex):
        self.myId = myId
        self.count = count
        self.mutex = mutex
        threading.Thread.__init__(self)
        
    def run(self):
        for i in range(self.count):
            with self.mutex:
                print('[%s] => %s' % (self.myId, i))
                
stdoutmutex = threading.Lock()   # same as thread.allocate_lock()
threads = []

for i in range(10):
    thread = Mythread(i, 100, stdoutmutex)
    thread.start()
    threads.append(thread)
    
for thread in threads:
    thread.join()
print('Main thread exiting.')
