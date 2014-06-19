"producer and consumer threads communicating with a shared queue"

numconsumers = 2
numproducers = 4
nummessages = 4

import threading, queue, time
safeprint = threading.Lock()
dataQueue = queue.Queue()
waitfor = []

def producer(idnum, aQueue):
    for msgnum in range(nummessages):
        time.sleep(idnum)
        aQueue.put('[producer id=%d, count=%d]' % (idnum, msgnum))

def consumer(idnum, aQueue):
    while True:
        time.sleep(0.1)
        try:
            data = aQueue.get(block=False)
        except queue.Empty:
            pass       
        else:
            with safeprint:
                print('consumer', idnum, 'got =>', data)

if __name__ == '__main__':
    for i in range(numconsumers):
        thread = threading.Thread(target=consumer, args=(i,dataQueue))
        thread.daemon = True  # else cannot exit
        thread.start()
        
    for i in range(numproducers):
        thread = threading.Thread(target=producer, args=(i, dataQueue))
        waitfor.append(thread)
        thread.start()

    for thread in waitfor: thread.join()        
    print('Main thread exiting.')