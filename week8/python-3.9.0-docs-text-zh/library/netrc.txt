"netrc" --- netrc 文件处理
**************************

**源代码:** Lib/netrc.py

======================================================================

"netrc" 类解析并封装了 Unix 的 **ftp** 程序和其他 FTP 客户端所使用的
netrc 文件格式。

class netrc.netrc([file])

   "netrc" 的实例或其子类的实例会被用来封装来自 netrc 文件的数据。 如
   果有初始化参数，它将指明要解析的文件。 如果未给出参数，则位于用户家
   目录的 ".netrc" 文件 -- 即 "os.path.expanduser()" 所确定的文件 --
   将会被读取。 在其他情况下，则将引发 "FileNotFoundError" 异常。 解析
   错误将引发 "NetrcParseError" 并附带诊断信息，包括文件名、行号以及终
   止令牌。 如果在 POSIX 系统上未指明参数，则当 ".netrc" 文件中有密码
   时，如果文件归属或权限不安全（归属的用户不是运行进程的用户，或者可
   供任何其他用户读取或写入）将引发 "NetrcParseError"。 这实现了与 ftp
   和其他使用 ".netrc" 的程序同等的安全行为。

   在 3.4 版更改: 添加了 POSIX 权限检查。

   在 3.7 版更改: 当未将 *file* 作为参数传入时会使用
   "os.path.expanduser()" 来查找 ".netrc" 文件的位置。

exception netrc.NetrcParseError

   当在源文本中遇到语法错误时由 "netrc" 类引发的异常。 此异常的实例提
   供了三个有用属性:  "msg" 为错误的文本说明，"filename" 为源文件的名
   称，而 "lineno" 给出了错误所在的行号。


netrc 对象
==========

"netrc" 实例具有下列方法:

netrc.authenticators(host)

   针对 *host* 的身份验证者返回一个 3 元组 "(login, account,
   password)"。 如果 netrc 文件不包含针对给定主机的条目，则返回关联到
   'default' 条目的元组。 如果匹配的主机或默认条目均不可用，则返回
   "None"。

netrc.__repr__()

   将类数据以 netrc 文件的格式转储为一个字符串。 （这会丢弃注释并可能
   重排条目顺序。）

"netrc" 的实例具有一些公共实例变量:

netrc.hosts

   将主机名映射到 "(login, account, password)" 元组的字典。 如果存在
   'default' 条目，则会表示为使用该名称的伪主机。

netrc.macros

   将宏名称映射到字符串列表的字典。

注解:

  密码会被限制为 ASCII 字符集的一个子集。 所有 ASCII 标点符号均可用作
  密码，但是要注意空白符和非打印字符不允许用作密码。 这是 .netrc 文件
  解析方式带来的限制，在未来可能会被解除。
