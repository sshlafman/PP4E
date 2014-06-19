"producer and consumer threads communicating with a shared queue"

numconsumers = 2
numproducers = 4
nummessages = 4

import _thread as thread, queue, time
safeprint = thread.allocate_lock()
dataQueue = queue.Queue()

def producer(idnum):
    for msgnum in range(nummessages):
        time.sleep(idnum)
        dataQueue.put('[producer id=%d, count=%d]' % (idnum, msgnum))

def consumer(idnum):
    while True:
        time.sleep(0.1)
        try:
            data = dataQueue.get(block=False)
        except queue.Empty:
            pass     
        else:
            with safeprint:
                print('consumer', idnum, 'got =>', data)

if __name__ == '__main__':
    for i in range(numconsumers):
        thread.start_new_thread(consumer, (i, ))
    for i in range(numproducers):
        thread.start_new_thread(producer, (i, ))
    time.sleep(((numproducers - 1) * nummessages) + 1)
    print('Main thread exiting.')