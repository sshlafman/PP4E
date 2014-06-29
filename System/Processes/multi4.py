"""
Process class can also be subclassed just like threading.Thread;
Queue works like queue.Queue but for cross-process,  not cross-thread
"""

import os, time, queue
from multiprocessing import Process, Queue               # process-safe shared queue
#                                                        # queue is a pipe + locks/semas

class Counter(Process):
    label = '  @'
    def __init__(self, start, queue):
        self.state = start
        self.post  = queue
        Process.__init__(self)
        
    def run(self):
        for i in range(3):
            time.sleep(1)                                   # simulates long-running task
            self.state += 1
            print(self.label, self.pid, self.state)         # self.pid is this child's pid
            self.post.put([self.pid, self.state])           # stdout file is shared by all
        print(self.label, self.pid, '-')
        
if __name__ == '__main__':
    print('start', os.getpid())
    expected = 9
    
    post = Queue()                                          # start 3 processes sharing queue
    p = Counter(0, post)                                    # children are producers
    q = Counter(100, post)
    r = Counter(1000, post)
    p.start(); q.start(); r.start()
    
    while expected:
        time.sleep(0.5)
        try:
            data = post.get(block=False)
        except queue.Empty:
            print('no data...')
        else:
            print('posted:', data)
            expected -= 1
    p.join(); q.join(); r.join()
    print('finish', os.getpid(), r.exitcode)                    # exitcode is child exit status 
    