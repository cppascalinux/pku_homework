"modulefinder" --- 查找脚本使用的模块
*************************************

**源码：** Lib/modulefinder.py

======================================================================

该模块提供了一个 "ModuleFinder" 类，可用于确定脚本导入的模块集。
"modulefinder.py" 也可以作为脚本运行，给出 Python 脚本的文件名作为参数
，之后将打印导入模块的报告。

modulefinder.AddPackagePath(pkg_name, path)

   记录名为 *pkg_name* 的包可以在指定的 *path* 中找到。

modulefinder.ReplacePackage(oldname, newname)

   允许指定名为 *oldname* 的模块实际上是名为 *newname* 的包。

class modulefinder.ModuleFinder(path=None, debug=0, excludes=[], replace_paths=[])

   该类提供 "run_script()" 和 "report()" 方法，用于确定脚本导入的模块
   集。 *path* 可以是搜索模块的目录列表；如果没有指定，则使用
   "sys.path" 。  *debug* 设置调试级别；更高的值使类打印调试消息，关于
   它正在做什么。 *excludes* 是要从分析中排除的模块名称列表。
   *replace_paths* 是将在模块路径中替换的 "(oldpath, newpath)" 元组的
   列表。

   report()

      将报告打印到标准输出，列出脚本导入的模块及其路径，以及缺少或似乎
      缺失的模块。

   run_script(pathname)

      分析 *pathname* 文件的内容，该文件必须包含 Python 代码。

   modules

      一个将模块名称映射到模块的字典。 请参阅 ModuleFinder 的示例用法
      。


"ModuleFinder" 的示例用法
=========================

稍后将分析的脚本（bacon.py）:

   import re, itertools

   try:
       import baconhameggs
   except ImportError:
       pass

   try:
       import guido.python.ham
   except ImportError:
       pass

将输出 bacon.py 报告的脚本:

   from modulefinder import ModuleFinder

   finder = ModuleFinder()
   finder.run_script('bacon.py')

   print('Loaded modules:')
   for name, mod in finder.modules.items():
       print('%s: ' % name, end='')
       print(','.join(list(mod.globalnames.keys())[:3]))

   print('-'*50)
   print('Modules not imported:')
   print('\n'.join(finder.badmodules.keys()))

输出样例（可能因架构而异）:

   Loaded modules:
   _types:
   copyreg:  _inverted_registry,_slotnames,__all__
   sre_compile:  isstring,_sre,_optimize_unicode
   _sre:
   sre_constants:  REPEAT_ONE,makedict,AT_END_LINE
   sys:
   re:  __module__,finditer,_expand
   itertools:
   __main__:  re,itertools,baconhameggs
   sre_parse:  _PATTERNENDERS,SRE_FLAG_UNICODE
   array:
   types:  __module__,IntType,TypeType
   ---------------------------------------------------
   Modules not imported:
   guido.python.ham
   baconhameggs
