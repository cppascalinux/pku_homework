"_thread" --- 底层多线程 API
****************************

======================================================================

该模块提供了操作多个线程（也被称为 *轻量级进程* 或 *任务*）的底层原语
—— 多个控制线程共享全局数据空间。为了处理同步问题，也提供了简单的锁机
制（也称为 *互斥锁* 或 *二进制信号*）。"threading" 模块基于该模块提供
了更易用的高级多线程 API。

在 3.7 版更改: 这个模块曾经是可选的，但现在总是可用的。

这个模块定义了以下常量和函数：

exception _thread.error

   发生线程相关错误时抛出。

   在 3.3 版更改: 现在是内建异常 "RuntimeError" 的别名。

_thread.LockType

   锁对象的类型。

_thread.start_new_thread(function, args[, kwargs])

   开启一个新线程并返回其标识。 线程执行函数 *function* 并附带参数列表
   *args* (必须是元组)。 可选的 *kwargs* 参数指定一个关键字参数字典。

   当函数返回时，线程会静默地退出。

   当函数因某个未处理异常而终结时，"sys.unraisablehook()" 会被调用以处
   理异常。 钩子参数的 *object* 属性为 *function*。 在默认情况下，会打
   印堆栈回溯然后该线程将退出（但其他线程会继续运行）。

   当函数引发 "SystemExit" 异常时，它会被静默地忽略。

   在 3.8 版更改: 现在会使用 "sys.unraisablehook()" 来处理未处理的异常
   。

_thread.interrupt_main()

   模拟一个 "signal.SIGINT" 信号到达主线程的效果。 线程可以使用这个函
   数来中断主线程。

   如果 Python 没有处理 "signal.SIGINT" (将它设为 "signal.SIG_DFL" 或
   "signal.SIG_IGN")，此函数将不做任何事。

_thread.exit()

   抛出 "SystemExit" 异常。如果没有捕获的话，这个异常会使线程退出。

_thread.allocate_lock()

   返回一个新的锁对象。锁中的方法在后面描述。初始情况下锁处于解锁状态
   。

_thread.get_ident()

   返回当前线程的 “线程描述符”。它是一个非零的整型数。它的值没有什么含
   义，主要是作为 magic cookie 使用，比如作为含有线程相关数据的字典的
   索引。线程描述符可能会在线程退出，新线程创建时复用。

_thread.get_native_id()

   返回内核分配给当前线程的原生集成线程 ID。 这是一个非负整数。 它的值
   可被用来在整个系统中唯一地标识这个特定线程（直到线程终结，在那之后
   该值可能会被 OS 回收再利用）。

   可用性: Windows, FreeBSD, Linux, macOS, OpenBSD, NetBSD, AIX。

   3.8 新版功能.

_thread.stack_size([size])

   返回新建线程时使用的堆栈大小。可选参数 *size* 指定之后新建的线程的
   堆栈大小，而且一定要是0（根据平台或者默认配置）或者最小是
   32,768(32KiB)的一个正整数。如果*size*没有指定，默认是0。如果不支持
   改变线程堆栈大小，会抛出 "RuntimeError" 错误。如果指定的堆栈大小不
   合法，会抛出 "ValueError" 错误并且不会修改堆栈大小。32KiB是当前最小
   的能保证解释器足够堆栈空间的堆栈大小。需要注意的是部分平台对于堆栈
   大小会有特定的限制，例如要求大于32KiB的堆栈大小或者需要根据系统内存
   页面的整数倍进行分配 - 应当查阅平台文档有关详细信息（4KiB页面比较普
   遍，在没有更具体信息的情况下，建议的方法是使用4096的倍数作为堆栈大
   小）

   可用性: Windows，具有 POSIX 线程的系统。

_thread.TIMEOUT_MAX

   "Lock.acquire()" 方法中 *timeout* 参数允许的最大值。传入超过这个值
   的 timeout 会抛出 "OverflowError" 异常。

   3.2 新版功能.

锁对象有以下方法：

lock.acquire(waitflag=1, timeout=-1)

   没有任何可选参数时，该方法无条件申请获得锁，有必要的话会等待其他线
   程释放锁（同时只有一个线程能获得锁 —— 这正是锁存在的原因）。

   如果传入了整型参数 *waitflag*，具体的行为取决于传入的值：如果是 0
   的话，只会在能够立刻获取到锁时才获取，不会等待，如果是非零的话，会
   像之前提到的一样，无条件获取锁。

   如果传入正浮点数参数 *timeout*，相当于指定了返回之前等待得最大秒数
   。如果传入负的 *timeout*，相当于无限期等待。如果 *waitflag* 是 0 的
   话，不能指定 *timeout*。

   如果成功获取到所会返回 "True"，否则返回 "False"。

   在 3.2 版更改: *timeout* 形参是新增的。

   在 3.2 版更改: 现在获取锁的操作可以被 POSIX 信号中断。

lock.release()

   释放锁。锁必须已经被获取过，但不一定是同一个线程获取的。

lock.locked()

   返回锁的状态：如果已被某个线程获取，返回 "True"，否则返回 "False"。

除了这些方法之外，锁对象也可以通过 "with" 语句使用，例如：

   import _thread

   a_lock = _thread.allocate_lock()

   with a_lock:
       print("a_lock is locked while this executes")

**注意事项：**

* 线程与中断奇怪地交互："KeyboardInterrupt" 异常可能会被任意一个线程捕
  获。（如果 "signal" 模块可用的话，中断总是会进入主线程。）

* 调用 "sys.exit()" 或是抛出 "SystemExit" 异常等效于调用
  "_thread.exit()"。

* 不可能中断锁的 "acquire()" 方法 —— "KeyboardInterrupt" 一场会在锁获
  取到之后发生。

* 当主线程退出时，由系统决定其他线程是否存活。在大多数系统中，这些线程
  会直接被杀掉，不会执行 "try" ... "finally" 语句，也不会执行对象析构
  函数。

* 当主线程退出时，不会进行正常的清理工作（除非使用了 "try" ...
  "finally" 语句），标准 I/O 文件也不会刷新。
