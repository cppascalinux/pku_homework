"posix" --- 最常见的 POSIX 系统调用
***********************************

======================================================================

此模块提供了对基于 C 标准和 POSIX 标准（一种稍加修改的 Unix 接口）进行
标准化的系统功能的访问。

**请勿直接导入此模块。** 而应导入 "os" 模块，它提供了此接口的 *可移植*
版本。 在 Unix 上，"os" 模块提供了 "posix" 接口的一个超集。 在非 Unix
操作系统上 "posix" 模块将不可用，但会通过 "os" 接口提供它的一个可用子
集。 一旦导入了 "os"，用它替代 "posix" 时就 *没有* 性能惩罚。 此外，
"os" 还提供了一些附加功能，例如在 "os.environ" 中的某个条目被修改时会
自动调用 "putenv()"。

错误将作为异常被报告；对于类型错误会给出普通异常，而系统调用所报告的异
常则会引发 "OSError"。


大文件支持
==========

某些操作系统（包括 AIX, HP-UX, Irix 和 Solaris）可对 "int" 和 "long"
为 32 位值的 C 编程模型提供大于 2 GiB 的文件的支持。 这在通常情况下是
以将相关数据长度和偏移类型定义为 64 位值的方式来实现的。 这样的文件有
时被称为 *大文件*。

Python 中的大文件支持会在 "off_t" 的大小超过 "long" 且 "long long" 至
少与 "off_t" 一样大时被启用。 要启用此模式可能必须在启用特定编译旗标的
情况下执行 Python 配置和编译。 例如，在最近几个版本的 Irix 中默认启用
了大文件支持，但在 Solaris 2.6 和 2.7 中你还需要执行这样的操作:

   CFLAGS="`getconf LFS_CFLAGS`" OPT="-g -O2 $CFLAGS" \
           ./configure

在支持大文件的 Linux 系统中，可以这样做:

   CFLAGS='-D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64' OPT="-g -O2 $CFLAGS" \
           ./configure


重要的模块内容
==============

除了 "os" 模块文档已说明的许多函数，"posix" 还定义了下列数据项:

posix.environ

   一个表示解释器启动时间点的字符串环境的字典。 键和值的类型在Unix 上
   为 bytes 而在 Windows 上为 str。 例如，"environ[b'HOME']" (Windows
   上的 "environ['HOME']") 是你的家目录的路径名，等价于 C 中的
   "getenv("HOME")"。

   修改此字典不会影响由 "execv()", "popen()" 或 "system()" 所传入的字
   符串环境；如果你需要修改环境，请将 "environ" 传给 "execve()" 或者为
   "system()" 或 "popen()" 的命令字符串添加变量赋值和 export 语句。

   在 3.2 版更改: 在 Unix 上，键和值为 bytes 类型。

   注解:

     "os" 模块提供了对 "environ" 的替代实现，它会在被修改时更新环境。
     还要注意更新 "os.environ" 将导致此字典失效。 推荐使用这个 "os" 模
     块版本而不是直接访问 "posix" 模块。
