"tty" --- 终端控制功能
**********************

**Source code:** Lib/tty.py

======================================================================

"tty" 模块定义了将 tty 放入 cbreak 和 raw 模式的函数。

因为它需要 "termios" 模块，所以只能在 Unix 上运行。

"tty" 模块定义了以下函数：

tty.setraw(fd, when=termios.TCSAFLUSH)

   将文件描述符 *fd* 的模式更改为 raw 。如果 *when* 被省略，则默认为
   "termios.TCSAFLUSH" ，并传递给 "termios.tcsetattr()" 。

tty.setcbreak(fd, when=termios.TCSAFLUSH)

   将文件描述符 *fd* 的模式更改为 cbreak 。如果 *when* 被省略，则默认
   为 "termios.TCSAFLUSH" ，并传递给 "termios.tcsetattr()" 。

参见:

  模块 "termios"
     低级终端控制接口。
