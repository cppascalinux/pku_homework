from multiprocessing import Process
import os
import time


def hello(i):
    print('son process id {} - for task {}'.format(os.getpid(), i))
    time.sleep(2)

if __name__=='__main__':
    print('current father process {}'.format(os.getpid()))
    start = time.time()
    p1 = Process(target=hello, args=(1,))
    p2 = Process(target=hello, args=(2,))
    p1.start() # start son process
    p2.start()
    p1.join() # wait until it finishes
    p2.join()
    end = time.time()
    print("Totally take {} seconds".format((end - start)))