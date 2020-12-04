from queue import Queue
import threading, time

# python queue中的Queue是线程安全的，不需要上锁

# 生产者类
class Producer(threading.Thread):
    def __init__(self, name, queue):
        threading.Thread.__init__(self, name=name)
        self.queue = queue

    def run(self):
        for i in range(1, 5):
            print("{} is producing {} to the queue!".format(self.getName(), i))
            self.queue.put(i)
            time.sleep(1)
        print("%s finished!" % self.getName())


# 消费者类
class Consumer(threading.Thread):
    def __init__(self, name, queue):
        threading.Thread.__init__(self, name=name)
        self.queue = queue

    def run(self):
        for i in range(1, 5):
            val = self.queue.get()
            print("{} is consuming {} in the queue.".format(self.getName(), val))
            time.sleep(1)
        print("%s finished!" % self.getName())


def main():
    queue = Queue()
    producer = Producer('Producer', queue)
    consumer = Consumer('Consumer', queue)

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()
    print('All threads finished!')


if __name__ == '__main__':
    main()