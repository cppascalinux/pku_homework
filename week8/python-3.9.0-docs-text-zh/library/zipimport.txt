"zipimport" --- 从 Zip 存档中导入模块
*************************************

**源代码：** Lib/zipimport.py

======================================================================

此模块添加了从 ZIP 格式档案中导入 Python 模块（ "*.py" ， "*.pyc" ）和
包的能力。通常不需要明确地使用 "zipimport" 模块，内置的 "import" 机制
会自动将此模块用于 ZIP 档案路径的 "sys.path" 项目上。

通常， "sys.path" 是字符串的目录名称列表。此模块同样允许 "sys.path" 的
一项成为命名 ZIP 文件档案的字符串。 ZIP 档案可以容纳子目录结构去支持包
的导入，并且可以将归档文件中的路径指定为仅从子目录导入。比如说，路径
"example.zip/lib/" 将只会从档案中的 "lib/" 子目录导入。

任何文件都可以存在于 ZIP档案之中，但是只有 ".py" 和 ".pyc" 文件是能够
导入的。不允许导入 ZIP 中的动态模组（ ".pyd" ， ".so" ）。请注意，如果
档案中只包含 ".py" 文件， Python不会尝试通过添加对应的 ".pyc" 文件修改
档案，意思是如果 ZIP 档案不包含 ".pyc" 文件，导入或许会变慢。

在 3.8 版更改: 以前，不支持带有档案注释的 ZIP 档案。

参见:

  PKZIP Application Note
     Phil Katz 编写的 ZIP 文件格式文档，此格式和使用的算法的创建者。

  **PEP 273** -  从ZIP压缩包导入模块
     由 James C. Ahlstrom 编写，他也提供了实现。 Python 2.3 遵循 **PEP
     273** 的规范，但是使用 Just van Rossum 编写的使用了 **PEP 302**
     中描述的导入钩的实现。

  **PEP 302** - 新导入钩
     PEP 添加导入钩来有助于模块运作。

此模块定义了一个异常：

exception zipimport.ZipImportError

   异常由 zipimporter 对象引发。这是 "ImportError" 的子类，因此，也可
   以捕获为 "ImportError" 。


zipimporter 对象
================

"zipimporter" 是用于导入 ZIP 文件的类。

class zipimport.zipimporter(archivepath)

   创建新的 zipimporter 实例。 *archivepath* 必须是指向 ZIP 文件的路径
   ，或者 ZIP 文件中的特定路径。例如， "foo/bar.zip/lib" 的
   *archivepath* 将在 ZIP 文件 "foo/bar.zip" 中的 "lib" 目录中查找模块
   （只要它存在）。

   如果 *archivepath* 没有指向一个有效的 ZIP 档案，引发
   "ZipImportError" 。

   find_module(fullname[, path])

      搜索由 *fullname* 指定的模块。 *fullname* 必须是完全合格的（点分
      的）模块名。它返回 zipimporter 实例本身如果模块被找到，或者返回
      "None" 如果没找到指定模块。可选的 *path* 被忽略，这是为了与导入
      器协议兼容。

   get_code(fullname)

      返回指定模块的代码对象。如果不能找到模块会引发 "ZipImportError"
      错误。

   get_data(pathname)

      返回与 *pathname* 相关联的数据。如果不能找到文件则引发 "OSError"
      错误。

      在 3.3 版更改: 曾经是 "IOError" 被引发而不是 "OSError" 。

   get_filename(fullname)

      如果导入了指定的模块 "__file__" ，则返回为该模块设置的值。如果未
      找到模块则引发 "ZipImportError" 错误。

      3.1 新版功能.

   get_source(fullname)

      返回指定模块的源代码。如果没有找到模块则引发 "ZipImportError" ，
      如果档案包含模块但是没有源代码，返回 "None" 。

   is_package(fullname)

      如果由 *fullname* 指定的模块是一个包则返回 "True" 。如果不能找到
      模块则引发 "ZipImportError" 错误。

   load_module(fullname)

      加载由 *fullname* 指定的模块。 *fullname* 必须是完全限定的（点分
      的）模块名。它返回已加载模块，或者当找不到模块时引发
      "ZipImportError" 错误。

   archive

      导入器关联的 ZIP 文件的文件名，没有可能的子路径。

   prefix

      ZIP 文件中搜索的模块的子路径。这是一个指向 ZIP 文件根目录的
      zipimporter 对象的空字符串。

   当与斜杠结合使用时， "archive" 和 "prefix" 属性等价于赋予
   "zipimporter" 构造器的原始 *archivepath* 参数。


示例
====

这是一个从 ZIP 档案中导入模块的例子 - 请注意 "zipimport" 模块不需要明
确地使用。

   $ unzip -l example.zip
   Archive:  example.zip
     Length     Date   Time    Name
    --------    ----   ----    ----
        8467  11-26-02 22:30   jwzthreading.py
    --------                   -------
        8467                   1 file
   $ ./python
   Python 2.3 (#1, Aug 1 2003, 19:54:32)
   >>> import sys
   >>> sys.path.insert(0, 'example.zip')  # Add .zip file to front of path
   >>> import jwzthreading
   >>> jwzthreading.__file__
   'example.zip/jwzthreading.py'
