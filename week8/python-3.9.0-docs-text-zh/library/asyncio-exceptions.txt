异常
****

**源代码:** Lib/asyncio/exceptions.py

======================================================================

exception asyncio.TimeoutError

   该操作已超过规定的截止日期。

   重要:

     这个异常与内置 "TimeoutError" 异常不同。

exception asyncio.CancelledError

   该操作已被取消。

   取消asyncio任务时，可以捕获此异常以执行自定义操作。在几乎所有情况下
   ，都必须重新引发异常。

   在 3.8 版更改: "CancelledError" 现在是 "BaseException" 的子类。

exception asyncio.InvalidStateError

   "Task" 或 "Future" 的内部状态无效。

   在为已设置结果值的未来对象设置结果值等情况下，可以引发此问题。

exception asyncio.SendfileNotAvailableError

   "sendfile" 系统调用不适用于给定的套接字或文件类型。

   子类 "RuntimeError" 。

exception asyncio.IncompleteReadError

   请求的读取操作未完全完成。

   由 asyncio stream APIs 提出

   此异常是 "EOFError" 的子类。

   expected

      预期字节的总数（ "int" ）。

   partial

      到达流结束之前读取的 "bytes" 字符串。

exception asyncio.LimitOverrunError

   在查找分隔符时达到缓冲区大小限制。

   由 asyncio stream APIs 提出

   consumed

      要消耗的字节总数。
