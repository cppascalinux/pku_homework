"fileinput" --- 迭代来自多个输入流的行
**************************************

**源代码:** Lib/fileinput.py

======================================================================

此模块实现了一个辅助类和一些函数用来快速编写访问标准输入或文件列表的循
环。 如果你只想要读写一个文件请参阅 "open()"。

典型用法为:

   import fileinput
   for line in fileinput.input():
       process(line)

此程序会迭代 "sys.argv[1:]" 中列出的所有文件内的行，如果列表为空则会使
用 "sys.stdin"。 如果有一个文件名为 "'-'"，它也会被替换为 "sys.stdin"
并且可选参数 *mode* 和 *openhook* 会被忽略。 要指定替代文件列表，请将
其作为第一个参数传给 "input()"。 也允许使用单个文件。

所有文件都默认以文本模式打开，但你可以通过在调用 "input()" 或
"FileInput" 时指定 *mode* 形参来重载此行为。 如果在打开或读取文件时发
生了 I/O 错误，将会引发 "OSError"。

在 3.3 版更改: 原来会引发 "IOError"；现在它是 "OSError" 的别名。

如果 "sys.stdin" 被使用超过一次，则第二次之后的使用将不返回任何行，除
非是被交互式的使用，或都是被显式地重置 (例如使用 "sys.stdin.seek(0)")
。

空文件打开后将立即被关闭；它们在文件列表中会被注意到的唯一情况只有当最
后打开的文件为空的时候。

反回的行不会对换行符做任何处理，这意味着文件中的最后一行可能不带换行符
。

想要控制文件的打开方式，你可以通过将 *openhook* 形参传给
"fileinput.input()" 或 "FileInput()" 来提供一个打开钩子。 此钩子必须为
一个函数，它接受两个参数，*filename* 和 *mode*，并返回一个以相应模式打
开的文件类对象。 此模块已经提供了两个有用的钩子。

以下函数是此模块的初始接口：

fileinput.input(files=None, inplace=False, backup='', *, mode='r', openhook=None)

   创建一个 "FileInput" 类的实例。 该实例将被用作此模块中函数的全局状
   态，并且还将在迭代期间被返回使用。 此函数的形参将被继续传递给
   "FileInput" 类的构造器。

   "FileInput" 实例可以在 "with" 语句中被用作上下文管理器。 在这个例子
   中，*input* 在 "with" 语句结束后将会被关闭，即使发生了异常也是如此:

      with fileinput.input(files=('spam.txt', 'eggs.txt')) as f:
          for line in f:
              process(line)

   在 3.2 版更改: 可以被用作上下文管理器。

   在 3.8 版更改: 关键字形参 *mode* 和 *openhook* 现在是仅限关键字形参
   。

下列函数会使用 "fileinput.input()" 所创建的全局状态；如果没有活动的状
态，则会引发 "RuntimeError"。

fileinput.filename()

   返回当前被读取的文件名。 在第一行被读取之前，返回 "None"。

fileinput.fileno()

   返回以整数表示的当前文件“文件描述符”。 当未打开文件时（处在第一行和
   文件之间），返回 "-1"。

fileinput.lineno()

   返回已被读取的累计行号。 在第一行被读取之前，返回 "0"。 在最后一个
   文件的最后一行被读取之后，返回该行的行号。

fileinput.filelineno()

   返回当前文件中的行号。 在第一行被读取之前，返回 "0"。 在最后一个文
   件的最后一行被读取之后，返回此文件中该行的行号。

fileinput.isfirstline()

   如果刚读取的行是其所在文件的第一行则返回 "True"，否则返回 "False"。

fileinput.isstdin()

   如果最后读取的行来自 "sys.stdin" 则返回 "True"，否则返回 "False"。

fileinput.nextfile()

   关闭当前文件以使下次迭代将从下一个文件（如果存在）读取第一行；不是
   从该文件读取的行将不会被计入累计行数。 直到下一个文件的第一行被读取
   之后文件名才会改变。 在第一行被读取之前，此函数将不会生效；它不能被
   用来跳过第一个文件。 在最后一个文件的最后一行被读取之后，此函数将不
   再生效。

fileinput.close()

   关闭序列。

此模块所提供的实现了序列行为的类同样也可用于子类化：

class fileinput.FileInput(files=None, inplace=False, backup='', *, mode='r', openhook=None)

   类 "FileInput" 是一个实现；它的方法 "filename()", "fileno()",
   "lineno()", "filelineno()", "isfirstline()", "isstdin()",
   "nextfile()" 和 "close()" 对应于此模块中具有相同名称的函数。 此外它
   还有一个 "readline()" 方法可返回下一个输入行，以及一个
   "__getitem__()" 方法，该方法实现了序列行为。 这种序列必须以严格的序
   列顺序来读写；随机读写和 "readline()" 不可以被混用。

   通过 *mode* 你可以指定要传给 "open()" 的文件模式。 它必须为 "'r'",
   "'rU'", "'U'" 和 "'rb'" 中的一个。

   *openhook* 如果给出则必须为一个函数，它接受两个参数 *filename* 和
   *mode*，并相应地返回一个打开的文件类对象。 你不能同时使用 *inplace*
   和 *openhook*。

   "FileInput" 实例可以在 "with" 语句中被用作上下文管理器。 在这个例子
   中，*input* 在 "with" 语句结束后将会被关闭，即使发生了异常也是如此:

      with FileInput(files=('spam.txt', 'eggs.txt')) as input:
          process(input)

   在 3.2 版更改: 可以被用作上下文管理器。

   3.4 版后已移除: "'rU'" 和 "'U'" 模式。

   3.8 版后已移除: 对 "__getitem__()" 方法的支持已弃用。

   在 3.8 版更改: 关键字形参 *mode* 和 *openhook* 现在是仅限关键字形参
   。

**可选的原地过滤:** 如果传递了关键字参数 "inplace=True" 给
"fileinput.input()" 或 "FileInput" 构造器，则文件会被移至备份文件并将
标准输出定向到输入文件（如果已存在与备份文件同名的文件，它将被静默地替
换）。 这使得编写一个能够原地重写其输入文件的过滤器成为可能。 如果给出
了 *backup* 形参 (通常形式为 "backup='.<some extension>'")，它将指定备
份文件的扩展名，并且备份文件会被保留；默认情况下扩展名为 "'.bak'" 并且
它会在输出文件关闭时被删除。 在读取标准输入时原地过滤会被禁用。

此模块提供了以下两种打开文件钩子：

fileinput.hook_compressed(filename, mode)

   使用 "gzip" 和 "bz2" 模块透明地打开 gzip 和 bzip2 压缩的文件（通过
   扩展名 "'.gz'" 和 "'.bz2'" 来识别）。 如果文件扩展名不是 "'.gz'" 或
   "'.bz2'"，文件会以正常方式打开（即使用 "open()" 并且不带任何解压操
   作）。

   使用示例:  "fi =
   fileinput.FileInput(openhook=fileinput.hook_compressed)"

fileinput.hook_encoded(encoding, errors=None)

   返回一个通过 "open()" 打开每个文件的钩子，使用给定的 *encoding* 和
   *errors* 来读取文件。

   使用示例: "fi =
   fileinput.FileInput(openhook=fileinput.hook_encoded("utf-8",
   "surrogateescape"))"

   在 3.6 版更改: 添加了可选的 *errors* 形参。
