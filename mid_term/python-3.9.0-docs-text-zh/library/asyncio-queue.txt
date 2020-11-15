队列集
******

**源代码:** Lib/asyncio/queues.py

======================================================================

asyncio 队列被设计成与 "queue" 模块类似。尽管 asyncio队列不是线程安全
的，但是他们是被设计专用于 async/await 代码。

注意asyncio 的队列没有 *timeout* 形参；请使用 "asyncio.wait_for()" 函
数为队列添加超时操作。

参见下面的 Examples 部分


队列
====

class asyncio.Queue(maxsize=0, *, loop=None)

   先进，先出（FIFO）队列

   如果 *maxsize* 小于等于零，则队列尺寸是无限的。如果是大于 "0" 的整
   数，则当队列达到 *maxsize* 时， "await put()" 将阻塞至某个元素被
   "get()" 取出。

   不像标准库中的并发型 "queue" ，队列的尺寸一直是已知的，可以通过调用
   "qsize()" 方法返回。

   Deprecated since version 3.8, will be removed in version 3.10:
   *loop* 形参。

   这个类 不是线程安全的。

   maxsize

      队列中可存放的元素数量。

   empty()

      如果队列为空返回 "True" ，否则返回 "False" 。

   full()

      如果有 "maxsize" 个条目在队列中，则返回 "True" 。

      如果队列用 "maxsize=0" （默认）初始化，则 "full()" 永远不会返回
      "True" 。

   coroutine get()

      从队列中删除并返回一个元素。如果队列为空，则等待，直到队列中有元
      素。

   get_nowait()

      立即返回一个队列中的元素，如果队列内有值，否则引发异常
      "QueueEmpty" 。

   coroutine join()

      阻塞至队列中所有的元素都被接收和处理完毕。

      当条目添加到队列的时候，未完成任务的计数就会增加。每当消费协程调
      用 "task_done()" 表示这个条目已经被回收，该条目所有工作已经完成
      ，未完成计数就会减少。当未完成计数降到零的时候， "join()" 阻塞被
      解除。

   coroutine put(item)

      添加一个元素进队列。如果队列满了，在添加元素之前，会一直等待空闲
      插槽可用。

   put_nowait(item)

      不阻塞的放一个元素入队列。

      如果没有立即可用的空闲槽，引发 "QueueFull" 异常。

   qsize()

      返回队列用的元素数量。

   task_done()

      表明前面排队的任务已经完成，即get出来的元素相关操作已经完成。

      由队列使用者控制。每个 "get()" 用于获取一个任务，任务最后调用
      "task_done()" 告诉队列，这个任务已经完成。

      如果 "join()" 当前正在阻塞，在所有条目都被处理后，将解除阻塞(意
      味着每个 "put()" 进队列的条目的 "task_done()" 都被收到)。

      如果被调用的次数多于放入队列中的项目数量，将引发 "ValueError" 。


优先级队列
==========

class asyncio.PriorityQueue

   "Queue" 的变体；按优先级顺序取出条目 (最小的先取出)。

   条目通常是 "(priority_number, data)" 形式的元组。


后进先出队列
============

class asyncio.LifoQueue

   "Queue" 的变体，先取出最近添加的条目（后进，先出）。


异常
====

exception asyncio.QueueEmpty

   当队列为空的时候，调用 "get_nowait()" 方法而引发这个异常。

exception asyncio.QueueFull

   当队列中条目数量已经达到它的 *maxsize* 的时候，调用 "put_nowait()"
   方法而引发的异常。


示例
====

队列能被用于多个的并发任务的工作量分配：

   import asyncio
   import random
   import time


   async def worker(name, queue):
       while True:
           # Get a "work item" out of the queue.
           sleep_for = await queue.get()

           # Sleep for the "sleep_for" seconds.
           await asyncio.sleep(sleep_for)

           # Notify the queue that the "work item" has been processed.
           queue.task_done()

           print(f'{name} has slept for {sleep_for:.2f} seconds')


   async def main():
       # Create a queue that we will use to store our "workload".
       queue = asyncio.Queue()

       # Generate random timings and put them into the queue.
       total_sleep_time = 0
       for _ in range(20):
           sleep_for = random.uniform(0.05, 1.0)
           total_sleep_time += sleep_for
           queue.put_nowait(sleep_for)

       # Create three worker tasks to process the queue concurrently.
       tasks = []
       for i in range(3):
           task = asyncio.create_task(worker(f'worker-{i}', queue))
           tasks.append(task)

       # Wait until the queue is fully processed.
       started_at = time.monotonic()
       await queue.join()
       total_slept_for = time.monotonic() - started_at

       # Cancel our worker tasks.
       for task in tasks:
           task.cancel()
       # Wait until all worker tasks are cancelled.
       await asyncio.gather(*tasks, return_exceptions=True)

       print('====')
       print(f'3 workers slept in parallel for {total_slept_for:.2f} seconds')
       print(f'total expected sleep time: {total_sleep_time:.2f} seconds')


   asyncio.run(main())
