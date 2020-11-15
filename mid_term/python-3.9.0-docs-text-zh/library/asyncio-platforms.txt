平台支持
********

"asyncio" 模块被设计为可移植的,但由于平台的底层架构和功能，一些平台存
在细微的差异和限制。


所有平台
========

* "loop.add_reader()" 和 "loop.add_writer()" 不能用来监视文件I/O。


Windows
=======

**源代码:** Lib/asyncio/proactor_events.py,
Lib/asyncio/windows_events.py, Lib/asyncio/windows_utils.py

======================================================================

在 3.8 版更改: 在 Windows 上，"ProactorEventLoop" 现在是默认的事件循环
。

Windows上的所有事件循环都不支持以下方法:

* 不支持 "loop.create_unix_connection()" 和
  "loop.create_unix_server()" 。 "socket.AF_UNIX" 套接字相关参数仅限于
  Unix。

* 不支持 "loop.add_signal_handler()" 和 "loop.remove_signal_handler()"
  。

"SelectorEventLoop" 有下列限制:

* "SelectSelector" 只被用于等待套接字事件：它支持套接字且最多支持512个
  套接字。

* "loop.add_reader()" 和 "loop.add_writer()" 只接受套接字处理回调函数(
  如管道、文件描述符等都不支持)。

* 因为不支持管道，所以  "loop.connect_read_pipe()" 和
  "loop.connect_write_pipe()" 方法没有实现。

* 不支持 Subprocesses ，也就是  "loop.subprocess_exec()" 和
  "loop.subprocess_shell()" 方法没有实现。

"ProactorEventLoop" 有下列限制:

* 不支持  "loop.add_reader()" 和 "loop.add_writer()" 方法。

Windows上单调时钟的分辨率大约为 15.6 毫秒。最佳的分辨率是 0.5 毫秒。分
辨率依赖于具体的硬件（HPET）和Windows的设置。


Windows的子进程支持
-------------------

在 Windows 上，默认的事件循环 "ProactorEventLoop" 支持子进程，而
"SelectorEventLoop" 则不支持。

也不支持 "policy.set_child_watcher()" 函数，"ProactorEventLoop" 有不同
的机制来监视子进程。


macOS
=====

完整支持流行的macOS版本。

-[ macOS <= 10.8 ]-

在 macOS 10.6, 10.7 和 10.8 上，默认的事件循环使用
"selectors.KqueueSelector"，在这些版本上它并不支持字符设备。 可以手工
配置 "SelectorEventLoop" 来使用 "SelectSelector" 或 "PollSelector" 以
在这些较老版本的 macOS 上支持字符设备。 例如:

   import asyncio
   import selectors

   selector = selectors.SelectSelector()
   loop = asyncio.SelectorEventLoop(selector)
   asyncio.set_event_loop(loop)
