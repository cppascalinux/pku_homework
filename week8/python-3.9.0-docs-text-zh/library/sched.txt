"sched" --- 事件调度器
**********************

**源码：** Lib/sched.py

======================================================================

"sched" 模块定义了一个实现通用事件调度程序的类：

class sched.scheduler(timefunc=time.monotonic, delayfunc=time.sleep)

   "scheduler" 类定义了一个调度事件的通用接口。 它需要两个函数来实际处
   理“外部世界” —— *timefunc* 应当不带参数地调用，并返回一个数字（“时
   间”，可以为任意单位）。 *delayfunc* 函数应当带一个参数调用，与
   *timefunc* 的输出相兼容，并且应当延迟其所指定的时间单位。 每个事件
   运行后还将调用 *delayfunc* 并传入参数 "0" 以允许其他线程有机会在多
   线程应用中运行。

   在 3.3 版更改: *timefunc* 和 *delayfunc* 参数是可选的。

   在 3.3 版更改: "scheduler" 类可以安全的在多线程环境中使用。

示例:

   >>> import sched, time
   >>> s = sched.scheduler(time.time, time.sleep)
   >>> def print_time(a='default'):
   ...     print("From print_time", time.time(), a)
   ...
   >>> def print_some_times():
   ...     print(time.time())
   ...     s.enter(10, 1, print_time)
   ...     s.enter(5, 2, print_time, argument=('positional',))
   ...     s.enter(5, 1, print_time, kwargs={'a': 'keyword'})
   ...     s.run()
   ...     print(time.time())
   ...
   >>> print_some_times()
   930343690.257
   From print_time 930343695.274 positional
   From print_time 930343695.275 keyword
   From print_time 930343700.273 default
   930343700.276


调度器对象
==========

"scheduler" 实例拥有以下方法和属性：

scheduler.enterabs(time, priority, action, argument=(), kwargs={})

   安排一个新事件。 *time* 参数应该有一个数字类型兼容的返回值，与传递
   给构造函数的 *timefunc* 函数的返回值兼容。 计划在相同 *time* 的事件
   将按其 *priority* 的顺序执行。 数字越小表示优先级越高。

   执行事件意为执行 "action(*argument, **kwargs)"。 *argument* 是包含
   有 *action* 的位置参数的序列。 *kwargs* 是包含 *action* 的关键字参
   数的字典。

   返回值是一个事件，可用于以后取消事件（ 参见 "cancel()" ）。

   在 3.3 版更改: *argument* 参数是可选的。

   在 3.3 版更改: 添加了 *kwargs* 形参。

scheduler.enter(delay, priority, action, argument=(), kwargs={})

   安排延后 *delay* 时间单位的事件。 除了相对时间，其他参数、效果和返
   回值与 "enterabs()" 的相同。

   在 3.3 版更改: *argument* 参数是可选的。

   在 3.3 版更改: 添加了 *kwargs* 形参。

scheduler.cancel(event)

   从队列中删除事件。 如果 *event* 不是当前队列中的事件，则此方法将引
   发 "ValueError"。

scheduler.empty()

   如果事件队列为空则返回 "True"。

scheduler.run(blocking=True)

   运行所有预定事件。 此方法将等待（使用传递给构造函数的 "delayfunc()"
   函数）进行下一个事件，然后执行它，依此类推，直到没有更多的计划事件
   。

   如果 *blocking* 为false，则执行由于最快到期（如果有）的预定事件，然
   后在调度程序中返回下一个预定调用的截止时间（如果有）。

   *action* 或 *delayfunc* 都可以引发异常。 在任何一种情况下，调度程序
   都将保持一致状态并传播异常。 如果 *action* 引发异常，则在将来调用
   "run()" 时不会尝试该事件。

   如果一系列事件的运行时间比下一个事件之前的可用时间长，那么调度程序
   将完全落后。 不会发生任何事件；调用代码负责取消不再相关的事件。

   在 3.3 版更改: 添加了 *blocking* 形参。

scheduler.queue

   只读属性按照将要运行的顺序返回即将发生的事件列表。 每个事件都显示为
   *named tuple* ，包含以下字段：time、priority、action、argument、
   kwargs。
