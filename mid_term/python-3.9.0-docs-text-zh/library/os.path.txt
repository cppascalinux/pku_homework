"os.path" --- 常用路径操作
**************************

**源代码：** Lib/posixpath.py （用于 POSIX）和 Lib/ntpath.py （用于
Windows NT）

======================================================================

该模块在路径名上实现了一些有用的功能：如需读取或写入文件，请参见
"open()" ；有关访问文件系统的信息，请参见 "os" 模块。路径参数可以字符
串或字节形式传递。我们鼓励应用程序将文件名表示为（Unicode）字符串。不
幸的是，某些文件名在Unix上可能无法用字符串表示，因此在Unix上平台上需要
支持任意文件名的应用程序，应使用字节对象来表示路径名。反之亦然，在
Windows平台上仅使用字节对象，不能表示的所有文件名（以标准 "mbcs" 编码
），因此Windows应用程序应使用字符串对象来访问所有文件。

与unix shell不同，Python不执行任何 *自动* 路径扩展。当应用程序需要类似
shell的路径扩展时，可以显式调用诸如 "expanduser()" 和 "expandvars()"
之类的函数。 （另请参见 "glob" 模块。）

参见: "pathlib" 模块提供高级路径对象。

注解:

  所有这些函数都仅接受字节或字符串对象作为其参数。如果返回路径或文件名
  ，则结果是相同类型的对象。

注解:

  由于不同的操作系统具有不同的路径名称约定，因此标准库中有此模块的几个
  版本。"os.path" 模块始终是适合 Python 运行的操作系统的路径模块，因此
  可用于本地路径。但是，如果操作的路径 *总是* 以一种不同的格式显示，那
  么也可以分别导入和使用各个模块。它们都具有相同的接口：

  * "posixpath" 用于Unix 样式的路径

  * "ntpath" 用于 Windows 路径

在 3.8 版更改: "exists()"、"lexists()"、"isdir()"、"isfile()"、
"islink()" 和 "ismount()" 现在遇到系统层面上不可表示的字符或字节的路径
时，会返回 "False"，而不是抛出异常。

os.path.abspath(path)

   返回路径 *path* 的绝对路径（标准化的）。在大多数平台上，这等同于用
   "normpath(join(os.getcwd(), path))" 的方式调用 "normpath()" 函数。

   在 3.6 版更改: 接受一个 *类路径对象*。

os.path.basename(path)

   返回路径 *path* 的基本名称。这是将 *path* 传入函数 "split()" 之后，
   返回的一对值中的第二个元素。请注意，此函数的结果与Unix **basename**
   程序不同。**basename** 在 "'/foo/bar/'" 上返回 "'bar'"，而
   "basename()" 函数返回一个空字符串 ("''")。

   在 3.6 版更改: 接受一个 *类路径对象*。

os.path.commonpath(paths)

   接受包含多个路径的序列 *paths*，返回 *paths* 的最长公共子路径。如果
   *paths* 同时包含绝对路径和相对路径，或 *paths* 在不同的驱动器上，或
   *paths* 为空，则抛出 "ValueError" 异常。与 "commonprefix()" 不同，
   本方法返回有效路径。

   可用性: Unix, Windows。

   3.5 新版功能.

   在 3.6 版更改: 接受一个 *类路径对象* 序列。

os.path.commonprefix(list)

   接受包含多个路径的 *列表*，返回所有路径的最长公共前缀（逐字符比较）
   。如果 *列表* 为空，则返回空字符串 ("''")。

   注解:

     此函数是逐字符比较，因此可能返回无效路径。要获取有效路径，参见
     "commonpath()"。

        >>> os.path.commonprefix(['/usr/lib', '/usr/local/lib'])
        '/usr/l'

        >>> os.path.commonpath(['/usr/lib', '/usr/local/lib'])
        '/usr'

   在 3.6 版更改: 接受一个 *类路径对象*。

os.path.dirname(path)

   返回路径 *path* 的目录名称。这是将 *path* 传入函数 "split()" 之后，
   返回的一对值中的第一个元素。

   在 3.6 版更改: 接受一个 *类路径对象*。

os.path.exists(path)

   如果 *path* 指向一个已存在的路径或已打开的文件描述符，返回 "True"。
   对于失效的符号链接，返回 "False"。在某些平台上，如果使用
   "os.stat()" 查询到目标文件没有执行权限，即使 *path* 确实存在，本函
   数也可能返回 "False"。

   在 3.3 版更改: *path* 现在可以是一个整数：如果该整数是一个已打开的
   文件描述符，返回 "True"，否则返回 "False"。

   在 3.6 版更改: 接受一个 *类路径对象*。

os.path.lexists(path)

   如果 *path* 指向一个已存在的路径，返回 "True"。对于失效的符号链接，
   也返回 "True"。在缺失 "os.lstat()" 的平台上等同于 "exists()"。

   在 3.6 版更改: 接受一个 *类路径对象*。

os.path.expanduser(path)

   在 Unix 和 Windows 上，将参数中开头部分的 "~" 或 "~user" 替换为当前
   *用户* 的家目录并返回。

   在 Unix 上，开头的 "~" 会被环境变量 "HOME" 代替，如果变量未设置，则
   通过内置模块 "pwd" 在 password 目录中查找当前用户的主目录。以
   "~user" 开头则直接在 password 目录中查找。

   在 Windows 上，如果设置了 "USERPROFILE"，就使用这个变量，否则会将
   "HOMEPATH" 和 "HOMEDRIVE" 结合在一起使用。以 "~user" 开头则将上述方
   法生成路径的最后一截目录替换成 user。

   如果展开路径失败，或者路径不是以波浪号开头，则路径将保持不变。

   在 3.6 版更改: 接受一个 *类路径对象*。

   在 3.8 版更改: Windows 不再使用 "HOME"。

os.path.expandvars(path)

   输入带有环境变量的路径作为参数，返回展开变量以后的路径。"$name" 或
   "${name}" 形式的子字符串被环境变量 *name* 的值替换。格式错误的变量
   名称和对不存在变量的引用保持不变。

   在 Windows 上，除了 "$name" 和 "${name}" 外，还可以展开 "%name%"。

   在 3.6 版更改: 接受一个 *类路径对象*。

os.path.getatime(path)

   返回 *path* 的最后访问时间。返回值是一个浮点数，为纪元秒数（参见
   "time" 模块）。如果该文件不存在或不可访问，则抛出 "OSError" 异常。

os.path.getmtime(path)

   返回 *path* 的最后修改时间。返回值是一个浮点数，为纪元秒数（参见
   "time" 模块）。如果该文件不存在或不可访问，则抛出 "OSError" 异常。

   在 3.6 版更改: 接受一个 *类路径对象*。

os.path.getctime(path)

   返回 *path* 在系统中的 ctime，在有些系统（比如 Unix）上，它是元数据
   的最后修改时间，其他系统（比如 Windows）上，它是 *path* 的创建时间
   。返回值是一个数，为纪元秒数（参见 "time" 模块）。如果该文件不存在
   或不可访问，则抛出 "OSError" 异常。

   在 3.6 版更改: 接受一个 *类路径对象*。

os.path.getsize(path)

   返回 *path* 的大小，以字节为单位。如果该文件不存在或不可访问，则抛
   出 "OSError" 异常。

   在 3.6 版更改: 接受一个 *类路径对象*。

os.path.isabs(path)

   如果 *path* 是一个绝对路径，则返回 "True"。在 Unix 上，它就是以斜杠
   开头，而在 Windows 上，它可以是去掉驱动器号后以斜杠（或反斜杠）开头
   。

   在 3.6 版更改: 接受一个 *类路径对象*。

os.path.isfile(path)

   如果 *path* 是 "现有的" 常规文件，则返回 "True"。本方法会跟踪符号链
   接，因此，对于同一路径，"islink()" 和 "isfile()" 都可能为 "True"。

   在 3.6 版更改: 接受一个 *类路径对象*。

os.path.isdir(path)

   如果 *path* 是 "现有的" 目录，则返回 "True"。本方法会跟踪符号链接，
   因此，对于同一路径，"islink()" 和 "isdir()" 都可能为 "True"。

   在 3.6 版更改: 接受一个 *类路径对象*。

os.path.islink(path)

   如果 *path* 指向的 "现有" 目录条目是一个符号链接，则返回 "True"。如
   果 Python 运行时不支持符号链接，则总是返回 "False"。

   在 3.6 版更改: 接受一个 *类路径对象*。

os.path.ismount(path)

   如果路径 *path* 是 *挂载点* （文件系统中挂载其他文件系统的点），则
   返回 "True"。在 POSIX 上，该函数检查 *path* 的父目录 "*path*/.." 是
   否在与 *path* 不同的设备上，或者 "*path*/.." 和 *path* 是否指向同一
   设备上的同一 inode（这一检测挂载点的方法适用于所有 Unix 和 POSIX 变
   体）。本方法不能可靠地检测同一文件系统上的绑定挂载 (bind mount)。在
   Windows 上，盘符和共享 UNC 始终是挂载点，对于任何其他路径，将调用
   "GetVolumePathName" 来查看它是否与输入的路径不同。

   3.4 新版功能: 支持在 Windows 上检测非根挂载点。

   在 3.6 版更改: 接受一个 *类路径对象*。

os.path.join(path, *paths)

   合理地拼接一个或多个路径部分。返回值是 *path* 和 **paths* 所有值的
   连接，每个非空部分后面都紧跟一个目录分隔符 ("os.sep")，除了最后一部
   分。这意味着如果最后一部分为空，则结果将以分隔符结尾。如果参数中某
   个部分是绝对路径，则绝对路径前的路径都将被丢弃，并从绝对路径部分开
   始连接。

   在 Windows 上，遇到绝对路径部分（例如 "r'\foo'"）时，不会重置盘符。
   如果某部分路径包含盘符，则会丢弃所有先前的部分，并重置盘符。请注意
   ，由于每个驱动器都有一个“当前目录”，所以 "os.path.join("c:",
   "foo")" 表示驱动器 "C:" 上当前目录的相对路径 ("c:foo")，而不是
   "c:\foo"。

   在 3.6 版更改: 接受一个 *类路径对象* 用于 *path* 和 *paths* 。

os.path.normcase(path)

   规范路径的大小写。在 Windows 上，将路径中的所有字符都转换为小写，并
   将正斜杠转换为反斜杠。在其他操作系统上返回原路径。

   在 3.6 版更改: 接受一个 *类路径对象*。

os.path.normpath(path)

   通过折叠多余的分隔符和对上级目录的引用来标准化路径名，所以 "A//B"、
   "A/B/"、"A/./B" 和 "A/foo/../B" 都会转换成 "A/B"。这个字符串操作可
   能会改变带有符号链接的路径的含义。在 Windows 上，本方法将正斜杠转换
   为反斜杠。要规范大小写，请使用 "normcase()"。

   在 3.6 版更改: 接受一个 *类路径对象*。

os.path.realpath(path)

   返回指定文件的规范路径，消除路径中存在的任何符号链接（如果操作系统
   支持）。

   注解:

     当发生符号链接循环时，返回的路径将是该循环的某个组成部分，但不能
     保证是哪个部分。

   在 3.6 版更改: 接受一个 *类路径对象*。

   在 3.8 版更改: 在 Windows 上现在可以正确解析符号链接和交接点
   (junction point)。

os.path.relpath(path, start=os.curdir)

   返回从当前目录或 *start* 目录（可选）到达 *path* 之间要经过的相对路
   径。这仅仅是对路径的计算，不会访问文件系统来确认 *path* 或 *start*
   的存在性或属性。

   *start* 默认为 "os.curdir"。

   可用性: Unix, Windows。

   在 3.6 版更改: 接受一个 *类路径对象*。

os.path.samefile(path1, path2)

   如果两个路径都指向相同的文件或目录，则返回 "True"。这由设备号和
   inode 号确定，在任一路径上调用 "os.stat()" 失败则抛出异常。

   可用性: Unix, Windows。

   在 3.2 版更改: 添加了 Windows 支持。

   在 3.4 版更改: Windows现在使用与其他所有平台相同的实现。

   在 3.6 版更改: 接受一个 *类路径对象*。

os.path.sameopenfile(fp1, fp2)

   如果文件描述符 *fp1* 和 *fp2* 指向相同文件，则返回 "True"。

   可用性: Unix, Windows。

   在 3.2 版更改: 添加了 Windows 支持。

   在 3.6 版更改: 接受一个 *类路径对象*。

os.path.samestat(stat1, stat2)

   如果 stat 元组 *stat1* 和 *stat2* 指向相同文件，则返回 "True"。这些
   stat 元组可能是由 "os.fstat()"、"os.lstat()" 或 "os.stat()" 返回的
   。本函数实现了 "samefile()" 和 "sameopenfile()" 底层所使用的比较过
   程。

   可用性: Unix, Windows。

   在 3.4 版更改: 添加了 Windows 支持。

   在 3.6 版更改: 接受一个 *类路径对象*。

os.path.split(path)

   将路径 *path* 拆分为一对，即 "(head, tail)"，其中，*tail* 是路径的
   最后一部分，而 *head* 里是除最后部分外的所有内容。*tail* 部分不会包
   含斜杠，如果 *path* 以斜杠结尾，则 *tail* 将为空。如果 *path* 中没
   有斜杠，*head* 将为空。如果 *path* 为空，则 *head* 和 *tail* 均为空
   。*head* 末尾的斜杠会被去掉，除非它是根目录（即它仅包含一个或多个斜
   杠）。在所有情况下，"join(head, tail)" 指向的位置都与 *path* 相同（
   但字符串可能不同）。另请参见函数 "dirname()" 和 "basename()"。

   在 3.6 版更改: 接受一个 *类路径对象*。

os.path.splitdrive(path)

   将路径 *path* 拆分为一对，即 "(drive, tail)"，其中 *drive* 是挂载点
   或空字符串。在没有驱动器概念的系统上，*drive* 将始终为空字符串。在
   所有情况下，"drive + tail" 都与 *path* 相同。

   在 Windows 上，本方法将路径拆分为驱动器/UNC 根节点和相对路径。

   如果路径 path 包含盘符，则 drive 将包含冒号及冒号前面的所有内容。例
   如 "splitdrive("c:/dir")" 返回 "("c:", "/dir")"。

   如果 path 是一个 UNC 路径，则 drive 将包含主机名和共享点，但不包括
   第四个分隔符。例如 "splitdrive("//host/computer/dir")" 返回
   "("//host/computer", "/dir")"。

   在 3.6 版更改: 接受一个 *类路径对象*。

os.path.splitext(path)

   将路径 *path* 拆分为一对，即 "(root, ext)"，使 "root + ext == path"
   ，其中 *ext* 为空或以英文句点开头，且最多包含一个句点。路径前的句点
   将被忽略，例如 "splitext('.cshrc')" 返回 "('.cshrc', '')"。

   在 3.6 版更改: 接受一个 *类路径对象*。

os.path.supports_unicode_filenames

   如果（在文件系统限制下）允许将任意 Unicode 字符串用作文件名，则为
   "True"。
