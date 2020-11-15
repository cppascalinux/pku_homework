"pickletools" --- pickle 开发者工具集
*************************************

**源代码:** Lib/pickletools.py

======================================================================

此模块包含与 "pickle" 模块内部细节有关的多个常量，一些关于具体实现的详
细注释，以及一些能够分析封存数据的有用函数。 此模块的内容对需要操作
"pickle" 的 Python 核心开发者来说很有用处；"pickle" 的一般用户则可能会
感觉 "pickletools" 模块与他们无关。


命令行语法
==========

3.2 新版功能.

当从命令行发起调用时，"python -m pickletools" 将对一个或更多 pickle 文
件的内容进行拆解。 请注意如果你查看 pickle 中保存的 Python 对象而非
pickle 格式的细节，你可能需要改用 "-m pickle"。 但是，当你想检查的
pickle 文件来自某个不受信任的源时，"-m pickletools" 是更安全的选择，因
为它不会执行 pickle 字节码。

例如，对于一个封存在文件 "x.pickle" 中的元组 "(1, 2)":

   $ python -m pickle x.pickle
   (1, 2)

   $ python -m pickletools x.pickle
       0: \x80 PROTO      3
       2: K    BININT1    1
       4: K    BININT1    2
       6: \x86 TUPLE2
       7: q    BINPUT     0
       9: .    STOP
   highest protocol among opcodes = 2


命令行选项
----------

-a, --annotate

   使用简短的操作码描述来标注每一行。

-o, --output=<file>

   输出应当写入到的文件名称。

-l, --indentlevel=<num>

   一个新的 MARK 层级所需缩进的空格数。

-m, --memo

   当反汇编多个对象时，保留各个反汇编的备忘记录。

-p, --preamble=<preamble>

   当指定一个以上的 pickle 文件时，在每次反汇编之前打印给定的前言。


编程接口
========

pickletools.dis(pickle, out=None, memo=None, indentlevel=4, annotate=0)

   将 pickle 的符号化反汇编数据输出到文件类对象 *out*，默认为
   "sys.stdout"。 *pickle* 可以是一个字符串或一个文件类对象。 *memo*
   可以是一个将被用作 pickle 的备忘记录的 Python 字典；它可被用来对由
   同一封存器创建的多个封存对象执行反汇编。 由 "MARK" 操作码指明的每个
   连续级别将会缩进 *indentlevel* 个空格。 如果为 *annotate* 指定了一
   个非零值，则输出中的每个操作码将以一个简短描述来标注。 *annotate*
   的值会被用作标注所应开始的列的提示。

   3.2 新版功能: *annotate* 参数。

pickletools.genops(pickle)

   提供包含 pickle 中所有操作码的 *iterator*，返回一个 "(opcode, arg,
   pos)" 三元组的序列。 *opcode* 是 "OpcodeInfo" 类的一个实例；*arg*
   是 Python 对象形式的 opcode 参数的已解码值；*pos* 是 opcode 所在的
   位置。 *pickle* 可以是一个字符串或一个文件类对象。

pickletools.optimize(picklestring)

   在消除未使用的 "PUT" 操作码之后返回一个新的等效 pickle 字符串。 优
   化后的 pickle 将更为简短，耗费更为的传输时间，要求更少的存储空间并
   能更高效地解封。
