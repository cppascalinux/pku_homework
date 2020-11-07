"queue" --- 一个同步的队列类
****************************

**源代码:** Lib/queue.py

======================================================================

"queue" 模块实现了多生产者、多消费者队列。这特别适用于消息必须安全地在
多线程间交换的线程编程。模块中的 "Queue" 类实现了所有所需的锁定语义。

模块实现了三种类型的队列，它们的区别仅仅是条目取回的顺序。在 FIFO
(first-in, first-out) 队列中，先添加的任务先取回。在 LIFO (last-in,
first-out) 队列中，最近被添加的条目先取回(操作类似一个堆栈)。优先级队
列中，条目将保持排序( 使用 "heapq" 模块 ) 并且最小值的条目第一个返回。

在内部，这三个类型的队列使用锁来临时阻塞竞争线程；然而，它们并未被设计
用于线程的重入性处理。

此外，模块实现了一个 "简单的"  FIFO (first-in, first-out) 队列类型，
"SimpleQueue" ，这个特殊实现为小功能在交换中提供额外的保障。

"queue" 模块定义了下列类和异常：

class queue.Queue(maxsize=0)

   Constructor for a FIFO (first-in, first-out) queue.  *maxsize* is
   an integer that sets the upperbound limit on the number of items
   that can be placed in the queue.  Insertion will block once this
   size has been reached, until queue items are consumed.  If
   *maxsize* is less than or equal to zero, the queue size is
   infinite.

class queue.LifoQueue(maxsize=0)

   LIFO (last-in, first-out) 队列构造函数。 *maxsize* 是个整数，用于设
   置可以放入队列中的项目数的上限。当达到这个大小的时候，插入操作将阻
   塞至队列中的项目被消费掉。如果 *maxsize* 小于等于零，队列尺寸为无限
   大。

class queue.PriorityQueue(maxsize=0)

   优先级队列构造函数。 *maxsize* 是个整数，用于设置可以放入队列中的项
   目数的上限。当达到这个大小的时候，插入操作将阻塞至队列中的项目被消
   费掉。如果 *maxsize* 小于等于零，队列尺寸为无限大。

   最小值先被取出( 最小值条目是由 "sorted(list(entries))[0]" 返回的条
   目)。条目的典型模式是一个以下形式的元组： "(priority_number, data)"
   。

   如果 *data* 元素没有可比性，数据将被包装在一个类中，忽略数据值，仅
   仅比较优先级数字 ：

      from dataclasses import dataclass, field
      from typing import Any

      @dataclass(order=True)
      class PrioritizedItem:
          priority: int
          item: Any=field(compare=False)

class queue.SimpleQueue

   无界的 FIFO (first-in, first-out) 队列构造函数。简单的队列，缺少任
   务跟踪等高级功能。

   3.7 新版功能.

exception queue.Empty

   对空的 "Queue" 对象，调用非阻塞的 "get()" (or  "get_nowait()") 时，
   引发的异常。

exception queue.Full

   对满的 "Queue" 对象，调用非阻塞的 "put()" (or "put_nowait()") 时，
   引发的异常。


Queue对象
=========

队列对象 ("Queue", "LifoQueue", 或者 "PriorityQueue") 提供下列描述的公
共方法。

Queue.qsize()

   返回队列的大致大小。注意，qsize() > 0 不保证后续的 get() 不被阻塞，
   qsize() < maxsize 也不保证 put() 不被阻塞。

Queue.empty()

   如果队列为空，返回 "True" ，否则返回 "False" 。如果 empty() 返回
   "True" ，不保证后续调用的 put() 不被阻塞。类似的，如果 empty() 返回
   "False" ，也不保证后续调用的 get() 不被阻塞。

Queue.full()

   如果队列是满的返回 "True" ，否则返回 "False" 。如果 full() 返回
   "True" 不保证后续调用的 get() 不被阻塞。类似的，如果 full() 返回
   "False" 也不保证后续调用的 put() 不被阻塞。

Queue.put(item, block=True, timeout=None)

   将 *item* 放入队列。如果可选参数 *block* 是 true 并且 *timeout* 是
   "None" (默认)，则在必要时阻塞至有空闲插槽可用。如果 *timeout* 是个
   正数，将最多阻塞 *timeout* 秒，如果在这段时间没有可用的空闲插槽，将
   引发 "Full" 异常。反之 (*block* 是 false)，如果空闲插槽立即可用，则
   把 *item* 放入队列，否则引发 "Full" 异常 ( 在这种情况下，*timeout*
   将被忽略)。

Queue.put_nowait(item)

   相当于 "put(item, False)" 。

Queue.get(block=True, timeout=None)

   从队列中移除并返回一个项目。如果可选参数 *block* 是 true 并且
   *timeout* 是 "None" (默认值)，则在必要时阻塞至项目可得到。如果
   *timeout* 是个正数，将最多阻塞 *timeout* 秒，如果在这段时间内项目不
   能得到，将引发 "Empty" 异常。反之 (*block* 是 false) , 如果一个项目
   立即可得到，则返回一个项目，否则引发 "Empty" 异常 (这种情况下，
   *timeout* 将被忽略)。

   POSIX系统3.0之前，以及所有版本的Windows系统中，如果 *block* 是 true
   并且 *timeout* 是 "None" ， 这个操作将进入基础锁的不间断等待。这意
   味着，没有异常能发生，尤其是 SIGINT 将不会触发 "KeyboardInterrupt"
   异常。

Queue.get_nowait()

   相当于 "get(False)" 。

提供了两个方法，用于支持跟踪 排队的任务 是否 被守护的消费者线程 完整的
处理。

Queue.task_done()

   表示前面排队的任务已经被完成。被队列的消费者线程使用。每个 "get()"
   被用于获取一个任务， 后续调用 "task_done()" 告诉队列，该任务的处理
   已经完成。

   如果 "join()" 当前正在阻塞，在所有条目都被处理后，将解除阻塞(意味着
   每个 "put()" 进队列的条目的 "task_done()" 都被收到)。

   如果被调用的次数多于放入队列中的项目数量，将引发 "ValueError" 异常
   。

Queue.join()

   阻塞至队列中所有的元素都被接收和处理完毕。

   当条目添加到队列的时候，未完成任务的计数就会增加。每当消费者线程调
   用 "task_done()" 表示这个条目已经被回收，该条目所有工作已经完成，未
   完成计数就会减少。当未完成计数降到零的时候， "join()" 阻塞被解除。

如何等待排队的任务被完成的示例：

   import threading, queue

   q = queue.Queue()

   def worker():
       while True:
           item = q.get()
           print(f'Working on {item}')
           print(f'Finished {item}')
           q.task_done()

   # turn-on the worker thread
   threading.Thread(target=worker, daemon=True).start()

   # send thirty task requests to the worker
   for item in range(30):
       q.put(item)
   print('All task requests sent\n', end='')

   # block until all tasks are done
   q.join()
   print('All work completed')


SimpleQueue 对象
================

"SimpleQueue" 对象提供下列描述的公共方法。

SimpleQueue.qsize()

   返回队列的大致大小。注意，qsize() > 0 不保证后续的 get() 不被阻塞。

SimpleQueue.empty()

   如果队列为空，返回 "True" ，否则返回 "False" 。如果 empty() 返回
   "False" ，不保证后续调用的 get() 不被阻塞。

SimpleQueue.put(item, block=True, timeout=None)

   将 *item* 放入队列。此方法永不阻塞，始终成功（除了潜在的低级错误，
   例如内存分配失败）。可选参数 *block* 和 *timeout* 仅仅是为了保持
   "Queue.put()" 的兼容性而提供，其值被忽略。

   **CPython implementation detail:** This method has a C
   implementation which is reentrant.  That is, a "put()" or "get()"
   call can be interrupted by another "put()" call in the same thread
   without deadlocking or corrupting internal state inside the queue.
   This makes it appropriate for use in destructors such as "__del__"
   methods or "weakref" callbacks.

SimpleQueue.put_nowait(item)

   相当于 "put(item)" ，仅为保持 "Queue.put_nowait()" 兼容性而提供。

SimpleQueue.get(block=True, timeout=None)

   从队列中移除并返回一个项目。如果可选参数 *block* 是 true 并且
   *timeout* 是 "None" (默认值)，则在必要时阻塞至项目可得到。如果
   *timeout* 是个正数，将最多阻塞 *timeout* 秒，如果在这段时间内项目不
   能得到，将引发 "Empty" 异常。反之 (*block* 是 false) , 如果一个项目
   立即可得到，则返回一个项目，否则引发 "Empty" 异常 (这种情况下，
   *timeout* 将被忽略)。

SimpleQueue.get_nowait()

   相当于 "get(False)" 。

参见:

  类 "multiprocessing.Queue"
     一个用于多进程上下文的队列类（而不是多线程）。

  "collections.deque" 是无界队列的一个替代实现，具有快速的不需要锁并且
  支持索引的原子化 "append()" 和 "popleft()" 操作。
