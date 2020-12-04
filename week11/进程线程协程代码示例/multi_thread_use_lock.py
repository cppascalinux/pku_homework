import threading
import time

def addone():
    global x, lock
    lock.acquire()
    for i in range(1000000):
        x = x + 1
    lock.release()

x = 0

lock = threading.Lock()
thread_list = []
t1 = threading.Thread(target=addone(), args=())
t2 = threading.Thread(target=addone(), args=())
t1.start()
t2.start()
t1.join()
t2.join()

print(x)