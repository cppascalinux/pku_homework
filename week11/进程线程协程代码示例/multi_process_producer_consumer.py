from multiprocessing import Process, Queue
import os, time, random

# 写数据进程执行的代码:
def producer(q):
    for value in range(5):
        print('Produce %d' % value)
        q.put(value)
        time.sleep(1)

# 读数据进程执行的代码:
def consumer(q):
    while True:
        value = q.get(True)
        print('Consume %d' % value)
        time.sleep(1)

if __name__=='__main__':
    t0 = time.time()
    # 父进程创建Queue，并传给各个子进程
    q = Queue()
    pw = Process(target=producer, args=(q,))
    pr = Process(target=consumer, args=(q,))
    # 启动子进程pw，写入
    pw.start()
    # 启动子进程pr，读取
    pr.start()
    # 等待pw结束:
    pw.join()
    # pr进程里是死循环，无法等待其结束，只能强行终止
    pr.terminate()
    print("Take %s s." % (time.time() - t0))