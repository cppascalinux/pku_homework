"getpass" --- 便携式密码输入工具
********************************

**源代码:** Lib/getpass.py

======================================================================

"getpass" 模块提供了两个函数：

getpass.getpass(prompt='Password: ', stream=None)

   提示用户输入一个密码且不会回显。 用户会看到字符串 *prompt* 作为提示
   ，其默认值为 "'Password: '"。 在 Unix 上，如有必要提示会使用替换错
   误句柄写入到文件类对象 *stream*。 *stream* 默认指向控制终端
   ("/dev/tty")，如果不可用则指向 "sys.stderr" (此参数在 Windows 上会
   被忽略)。

   如果回显自由输入不可用则 getpass() 将回退为打印一条警告消息到
   *stream* 并且从 "sys.stdin" 读取同时发出 "GetPassWarning"。

   注解:

     如果你从 IDLE 内部调用 getpass，输入可能是在你启动 IDLE 的终端中
     而非在 IDEL 窗口本身中完成。

exception getpass.GetPassWarning

   一个当密码输入可能被回显时发出的 "UserWarning" 子类。

getpass.getuser()

   返回用户的“登录名称”。

   此函数会按顺序检查环境变量 "LOGNAME", "USER", "LNAME" 和 "USERNAME"
   ，并返回其中第一个被设置为非空字符串的值。 如果均未设置，则在支持
   "pwd" 模块的系统上将返回来自密码数据库的登录名，否则将引发一个异常
   。

   通常情况下，此函数应优先于 "os.getlogin()" 使用。
