import threading
import time

def hello(i):
    print('thread id: {} for task {}'.format(threading.current_thread().name, i))
    time.sleep(2)

start = time.time()
    
t1 = threading.Thread(target=hello, args=(1,))
t2 = threading.Thread(target=hello, args=(2,))
t1.start()
t2.start()
t1.join()
t2.join()

end = time.time()
print("Take {} s".format((end - start)))