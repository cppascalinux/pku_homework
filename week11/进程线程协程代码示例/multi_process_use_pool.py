from multiprocessing import Process, Pool
import os
import time


def hello(i):
    print('son process id {} - for task {}'.format(os.getpid(), i))
    time.sleep(1)

if __name__=='__main__':
    print('current father process {}'.format(os.getpid()))
    start = time.time()
    p = Pool(4) # 4 kernel CPU.
    for i in range(5):
        p.apply_async(hello, args=(i,))
    p.close() # no longer receive new process
    p.join() # wait until all processes in the pool finishes
    end = time.time()
    print("Totally take {} seconds".format((end - start)))