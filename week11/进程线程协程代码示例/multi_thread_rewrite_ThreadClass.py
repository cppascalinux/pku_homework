import time, threading

def hello(i):
    time.sleep(2)
    return i*i

class MyThread(threading.Thread):
    def __init__(self, func, args , name='', ):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.name = name
        self.result = None

    def run(self):
        self.result = self.func(self.args[0],)
        print("result for %s : %d" % (self.name, self.result))
        
if __name__=='__main__':
    start = time.time()
    
    t1 = MyThread(hello, args=(1,), name = "t1")
    t2 = MyThread(hello, args=(2,), name = "t2")
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    
    end = time.time()
    print("Take {} s".format((end - start)))
    
# result

# result for t2 : 4
# result for t1 : 1
# Take 2.0020065307617188 s