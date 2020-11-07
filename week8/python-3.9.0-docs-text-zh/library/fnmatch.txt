"fnmatch" --- Unix 文件名模式匹配
*********************************

**源代码:** Lib/fnmatch.py

======================================================================

此模块提供了 Unix shell 风格的通配符，它们 *并不* 等同于正则表达式（关
于后者的文档参见 "re" 模块）。 shell 风格通配符所使用的特殊字符如下：

+--------------+--------------------------------------+
| 模式         | 意义                                 |
|==============|======================================|
| "*"          | 匹配所有                             |
+--------------+--------------------------------------+
| "?"          | 匹配任何单个字符                     |
+--------------+--------------------------------------+
| "[seq]"      | 匹配 *seq* 中的任何字符              |
+--------------+--------------------------------------+
| "[!seq]"     | 匹配任何不在 *seq* 中的字符          |
+--------------+--------------------------------------+

对于字面值匹配，请将原字符用方括号括起来。 例如，"'[?]'" 将匹配字符
"'?'"。

注意文件名分隔符 (Unix 上为 "'/'") *不是* 此模块所特有的。 请参见
"glob" 模块了解文件名扩展 ("glob" 使用 "filter()" 来匹配文件名的各个部
分)。 类似地，以一个句点打头的文件名也不是此模块所特有的，可以通过 "*"
和 "?" 模式来匹配。

fnmatch.fnmatch(filename, pattern)

   检测 *filename* 字符串是否匹配 *pattern* 字符串，返回 "True" 或
   "False"。 两个形参都会使用 "os.path.normcase()" 进行大小写正规化。
   "fnmatchcase()" 可被用于执行大小写敏感的比较，无论这是否为所在操作
   系统的标准。

   这个例子将打印当前目录下带有扩展名 ".txt" 的所有文件名:

      import fnmatch
      import os

      for file in os.listdir('.'):
          if fnmatch.fnmatch(file, '*.txt'):
              print(file)

fnmatch.fnmatchcase(filename, pattern)

   检测 *filename* 是否匹配 *pattern*，返回 "True" 或 "False"；此比较
   是大小写敏感的，并且不会应用 "os.path.normcase()"。

fnmatch.filter(names, pattern)

   返回 *names* 列表中匹配 *pattern* 的子集。 它等价于 "[n for n in
   names if fnmatch(n, pattern)]"，但其实现更为高效。

fnmatch.translate(pattern)

   返回 shell 风格 *pattern* 转换成的正则表达式以便用于 "re.match()"。

   示例:

   >>> import fnmatch, re
   >>>
   >>> regex = fnmatch.translate('*.txt')
   >>> regex
   '(?s:.*\\.txt)\\Z'
   >>> reobj = re.compile(regex)
   >>> reobj.match('foobar.txt')
   <re.Match object; span=(0, 10), match='foobar.txt'>

参见:

  模块 "glob"
     Unix shell 风格路径扩展。
