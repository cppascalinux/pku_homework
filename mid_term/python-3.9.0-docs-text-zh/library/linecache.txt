"linecache" --- 随机读写文本行
******************************

**源代码:** Lib/linecache.py

======================================================================

"linecache" 模块允许从一个 Python 源文件中获取任意的行，并会尝试使用缓
存进行内部优化，常应用于从单个文件读取多行的场合。 此模块被
"traceback" 模块用来提取源码行以便包含在格式化的回溯中。

"tokenize.open()" 函数被用于打开文件。 此函数使用
"tokenize.detect_encoding()" 来获取文件的编码格式；如果未指明编码格式
，则默认编码为 UTF-8。

"linecache" 模块定义了下列函数：

linecache.getline(filename, lineno, module_globals=None)

   从名为 *filename* 的文件中获取 *lineno* 行，此函数绝不会引发异常
   --- 出现错误时它将返回 "''" (所有找到的行都将包含换行符作为结束)。

   如果找不到名为 *filename* 的文件，此函数会先在 *module_globals* 中
   检查 **PEP 302** "__loader__"。 如果存在这样的加载器并且它定义了
   "get_source" 方法，则由该方法来确定源行 (如果 "get_source()" 返回
   "None"，则该函数返回 "''")。 最后，如果 *filename* 是一个相对路径文
   件名，则它会在模块搜索路径 "sys.path" 中按条目的相对位置进行查找。

linecache.clearcache()

   清空缓存。 如果你不再需要之前使用 "getline()" 从文件读取的行即可使
   用此函数。

linecache.checkcache(filename=None)

   检查缓存有效性。 如果缓存中的文件在磁盘上发生了改变，而你需要更新后
   的版本即可使用此函数。 如果省略了 *filename*，它会检查缓存中的所有
   条目。

linecache.lazycache(filename, module_globals)

   捕获有关某个非基于文件的模块的足够细节信息，以允许稍后再通过
   "getline()" 来获取其中的行，即使当稍后调用时 *module_globals* 为
   "None"。 这可以避免在实际需要读取行之前执行 I/O，也不必始终保持模块
   全局变量。

   3.5 新版功能.

示例:

   >>> import linecache
   >>> linecache.getline(linecache.__file__, 8)
   'import sys\n'
