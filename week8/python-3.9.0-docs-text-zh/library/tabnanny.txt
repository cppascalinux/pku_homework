"tabnanny" --- 模糊缩进检测
***************************

**源代码:** Lib/tabnanny.py

======================================================================

目前，该模块旨在作为脚本调用。但是可以使用下面描述的 "check()" 函数将
其导入IDE。

注解:

  此模块提供的API可能会在将来的版本中更改；此类更改可能无法向后兼容。

tabnanny.check(file_or_dir)

   如果 *file_or_dir* 是目录而非符号链接，则递归地在名为 *file_or_dir*
   的目录树中下行，沿途检查所有 ".py" 文件。 如果 *file_or_dir* 是一个
   普通 Python 源文件，将检查其中的空格相关问题。 诊断消息将使用
   "print()" 函数写入到标准输出。

tabnanny.verbose

   此旗标指明是否打印详细消息。 如果作为脚本调用则是通过 "-v" 选项来增
   加。

tabnanny.filename_only

   此旗标指明是否只打印包含空格相关问题文件的文件名。 如果作为脚本调用
   则是通过 "-q" 选项来设为真值。

exception tabnanny.NannyNag

   如果检测到模糊缩进则由 "process_tokens()" 引发。 在 "check()" 中捕
   获并处理。

tabnanny.process_tokens(tokens)

   此函数由 "check()" 用来处理由 "tokenize" 模块所生成的标记。

参见:

  模块 "tokenize"
     用于Python源代码的词法扫描程序。
