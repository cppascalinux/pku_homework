扩展/嵌入常见问题
*****************


可以使用 C 语言创建自己的函数吗？
=================================

是的，您可以在C中创建包含函数、变量、异常甚至新类型的内置模块。在文档
扩展和嵌入 Python 解释器 中有说明。

大多数中级或高级的Python书籍也涵盖这个主题。


可以使用 C++ 语言创建自己的函数吗？
===================================

是的，可以使用C ++中兼容C的功能。 在Python include文件周围放置`
*extern“C”{...}`* ，并在Python解释器调用的每个函数之前放置 "extern“C”"
。 具有构造函数的全局或静态C ++对象可能不是一个好主意。


C很难写，有没有其他选择？
=========================

编写自己的C扩展有很多选择，具体取决于您要做的事情。

Cython 及其相关的 Pyrex 是接受稍微修改过的Python形式并生成相应C代码的
编译器。 Cython和Pyrex可以编写扩展而无需学习Python的C API。

如果需要连接到某些当前不存在Python扩展的C或C ++库，可以尝试使用 SWIG
等工具包装库的数据类型和函数。  SIP ， CXX Boost , 或 Weave 也是包装C
++库的替代方案。


如何在 C 中执行任意 Python 语句？
=================================

执行此操作的最高层级函数为 "PyRun_SimpleString()"，它接受单个字符串参
数用于在模块 "__main__" 的上下文中执行并在成功时返回 "0" 而在发生异常
(包括 "SyntaxError") 时返回 "-1"。 如果你想要更多可控性，可以使用
"PyRun_String()"；请在 "Python/pythonrun.c" 中查看
"PyRun_SimpleString()" 的源码。


如何在 C 中对任意 Python 表达式求值？
=====================================

可以调用前一问题中介绍的函数 "PyRun_String()" 并附带起始标记符
"Py_eval_input"；它会解析表达式，对其求值并返回结果值。


如何从Python对象中提取C的值？
=============================

这取决于对象的类型。 如果是元组，"PyTuple_Size()" 可返回其长度而
"PyTuple_GetItem()" 可返回指定序号上的项。 对于列表也有类似的函数
"PyListSize()" 和 "PyList_GetItem()"。

对于字节串，"PyBytes_Size()" 可返回其长度而
"PyBytes_AsStringAndSize()" 提供一个指向其值和长度的指针。 请注意
Python 字节串可能为空，因此 C 的 "strlen()" 不应被使用。

要检测一个对象的类型，首先要确保它不为 "NULL"，然后使用
"PyBytes_Check()", "PyTuple_Check()", "PyList_Check()" 等等。

还有一个针对 Python 对象的高层级 API，通过所谓的‘抽象’接口提供 —— 请参
阅 "Include/abstract.h" 了解详情。 它允许使用 "PySequence_Length()",
"PySequence_GetItem()" 这样的调用来与任意种类的 Python 序列进行对接，
此外还可使用许多其他有用的协议例如数字 ("PyNumber_Index()" 等) 以及
PyMapping API 中的各种映射等等。


如何使用Py_BuildValue()创建任意长度的元组？
===========================================

不可以。应该使用 "PyTuple_Pack()" 。


如何从C调用对象的方法？
=======================

可以使用 "PyObject_CallMethod()" 函数来调用某个对象的任意方法。 形参为
该对象、要调用的方法名、类似 "Py_BuildValue()" 所用的格式字符串以及要
传给方法的参数值:

   PyObject *
   PyObject_CallMethod(PyObject *object, const char *method_name,
                       const char *arg_format, ...);

这适用于任何具有方法的对象 —— 不论是内置方法还是用户自定义方法。 你需
要负责对返回值进行最终的 "Py_DECREF()" 处理。

例如调用某个文件对象的 "seek" 方法并传入参数 10, 0 (假定文件对象的指针
为 "f"):

   res = PyObject_CallMethod(f, "seek", "(ii)", 10, 0);
   if (res == NULL) {
           ... an exception occurred ...
   }
   else {
           Py_DECREF(res);
   }

请注意由于 "PyObject_CallObject()" *总是* 接受一个元组作为参数列表，要
调用不带参数的函数，则传入格式为 "()"，要调用只带一个参数的函数，则应
将参数包含于圆括号中，例如 "(i)"。


如何捕获PyErr_Print()（或打印到stdout / stderr的任何内容）的输出？
==================================================================

在 Python 代码中，定义一个支持 "write()" 方法的对象。 将此对象赋值给
"sys.stdout" 和 "sys.stderr"。 调用 print_error 或者只是允许标准回溯机
制生效。 在此之后，输出将转往你的 "write()" 方法所指向的任何地方。

做到这一点的最简单方式是使用 "io.StringIO" 类：

   >>> import io, sys
   >>> sys.stdout = io.StringIO()
   >>> print('foo')
   >>> print('hello world!')
   >>> sys.stderr.write(sys.stdout.getvalue())
   foo
   hello world!

实现同样效果的自定义对象看起来是这样的：

   >>> import io, sys
   >>> class StdoutCatcher(io.TextIOBase):
   ...     def __init__(self):
   ...         self.data = []
   ...     def write(self, stuff):
   ...         self.data.append(stuff)
   ...
   >>> import sys
   >>> sys.stdout = StdoutCatcher()
   >>> print('foo')
   >>> print('hello world!')
   >>> sys.stderr.write(''.join(sys.stdout.data))
   foo
   hello world!


如何从C访问用Python编写的模块？
===============================

你可以通过如下方式获得一个指向模块对象的指针:

   module = PyImport_ImportModule("<modulename>");

如果模块尚未被导入（即它还不存在于 "sys.modules" 中），这会初始化该模
块；否则它只是简单地返回 "sys.modules["<modulename>"]" 的值。 请注意它
并不会将模块加入任何命名空间 —— 它只是确保模块被初始化并存在于
"sys.modules" 中。

之后你就可以通过如下方式来访问模块的属性（即模块中定义的任何名称）:

   attr = PyObject_GetAttrString(module, "<attrname>");

调用 "PyObject_SetAttrString()" 为模块中的变量赋值也是可以的。


如何在 Python 中对接 C ++ 对象？
================================

根据你的需求，可以选择许多方式。 手动的实现方式请查阅 "扩展与嵌入" 文
档 来入门。 需要知道的是对于 Python 运行时系统来说，C 和 C++ 并不没有
太大的区别 —— 因此围绕一个 C 结构（指针）类型构建新 Python 对象的策略
同样适用于 C++ 对象。

有关C ++库，请参阅 C很难写，有没有其他选择？


我使用Setup文件添加了一个模块，为什么make失败了？
=================================================

安装程序必须以换行符结束，如果没有换行符，则构建过程将失败。 （修复这
个需要一些丑陋的shell脚本编程，而且这个bug很小，看起来不值得花这么大力
气。)


如何调试扩展？
==============

将GDB与动态加载的扩展名一起使用时，在加载扩展名之前，不能在扩展名中设
置断点。

在您的 ".gdbinit" 文件中（或交互式）添加命令：

   br _PyImport_LoadDynamicModule

然后运行GDB：

   $ gdb /local/bin/python
   gdb) run myscript.py
   gdb) continue # repeat until your extension is loaded
   gdb) finish   # so that your extension is loaded
   gdb) br myfunction.c:50
   gdb) continue


我想在Linux系统上编译一个Python模块，但是缺少一些文件。为什么?
==============================================================

大多数打包的Python版本不包含 "/usr/lib/python2.*x*/config/" 目录，该目
录中包含编译Python扩展所需的各种文件。

对于Red Hat，安装python-devel RPM以获取必要的文件。

对于Debian，运行 "apt-get install python-dev" 。


如何区分“输入不完整”和“输入无效”？
==================================

有时，希望模仿Python交互式解释器的行为，在输入不完整时(例如，您键入了
“if”语句的开头，或者没有关闭括号或三个字符串引号)，给出一个延续提示，
但当输入无效时，立即给出一条语法错误消息。

在Python中，您可以使用 "codeop" 模块，该模块非常接近解析器的行为。例如
，IDLE就使用了这个。

在C中执行此操作的最简单方法是调用 "PyRun_InteractiveLoop()" （可能在单
独的线程中）并让Python解释器为您处理输入。您还可以设置
"PyOS_ReadlineFunctionPointer()" 指向您的自定义输入函数。有关更多提示
，请参阅 "Modules/readline.c" 和 "Parser/myreadline.c" 。

但是，有时必须在与其他应用程序相同的线程中运行嵌入式Python解释器，并且
不能允许 "PyRun_InteractiveLoop()" 在等待用户输入时停止。那么另一个解
决方案是调用 "PyParser_ParseString()" 并测试 "e.error" 等于 "E_EOF" ，
如果等于，就意味着输入不完整。这是一个示例代码片段，未经测试，灵感来自
Alex Farber的代码:

   #define PY_SSIZE_T_CLEAN
   #include <Python.h>
   #include <node.h>
   #include <errcode.h>
   #include <grammar.h>
   #include <parsetok.h>
   #include <compile.h>

   int testcomplete(char *code)
     /* code should end in \n */
     /* return -1 for error, 0 for incomplete, 1 for complete */
   {
     node *n;
     perrdetail e;

     n = PyParser_ParseString(code, &_PyParser_Grammar,
                              Py_file_input, &e);
     if (n == NULL) {
       if (e.error == E_EOF)
         return 0;
       return -1;
     }

     PyNode_Free(n);
     return 1;
   }

另一个解决方案是尝试使用 "Py_CompileString()" 编译接收到的字符串。如果
编译时没有出现错误，请尝试通过调用 "PyEval_EvalCode()" 来执行返回的代
码对象。否则，请将输入保存到以后。如果编译失败，找出是错误还是只需要更
多的输入-从异常元组中提取消息字符串，并将其与字符串 “分析时意外的EOF”
进行比较。下面是使用GNUreadline库的完整示例(您可能希望在调用readline()
时忽略 **SIGINT** )：

   #include <stdio.h>
   #include <readline.h>

   #define PY_SSIZE_T_CLEAN
   #include <Python.h>
   #include <object.h>
   #include <compile.h>
   #include <eval.h>

   int main (int argc, char* argv[])
   {
     int i, j, done = 0;                          /* lengths of line, code */
     char ps1[] = ">>> ";
     char ps2[] = "... ";
     char *prompt = ps1;
     char *msg, *line, *code = NULL;
     PyObject *src, *glb, *loc;
     PyObject *exc, *val, *trb, *obj, *dum;

     Py_Initialize ();
     loc = PyDict_New ();
     glb = PyDict_New ();
     PyDict_SetItemString (glb, "__builtins__", PyEval_GetBuiltins ());

     while (!done)
     {
       line = readline (prompt);

       if (NULL == line)                          /* Ctrl-D pressed */
       {
         done = 1;
       }
       else
       {
         i = strlen (line);

         if (i > 0)
           add_history (line);                    /* save non-empty lines */

         if (NULL == code)                        /* nothing in code yet */
           j = 0;
         else
           j = strlen (code);

         code = realloc (code, i + j + 2);
         if (NULL == code)                        /* out of memory */
           exit (1);

         if (0 == j)                              /* code was empty, so */
           code[0] = '\0';                        /* keep strncat happy */

         strncat (code, line, i);                 /* append line to code */
         code[i + j] = '\n';                      /* append '\n' to code */
         code[i + j + 1] = '\0';

         src = Py_CompileString (code, "<stdin>", Py_single_input);

         if (NULL != src)                         /* compiled just fine - */
         {
           if (ps1  == prompt ||                  /* ">>> " or */
               '\n' == code[i + j - 1])           /* "... " and double '\n' */
           {                                               /* so execute it */
             dum = PyEval_EvalCode (src, glb, loc);
             Py_XDECREF (dum);
             Py_XDECREF (src);
             free (code);
             code = NULL;
             if (PyErr_Occurred ())
               PyErr_Print ();
             prompt = ps1;
           }
         }                                        /* syntax error or E_EOF? */
         else if (PyErr_ExceptionMatches (PyExc_SyntaxError))
         {
           PyErr_Fetch (&exc, &val, &trb);        /* clears exception! */

           if (PyArg_ParseTuple (val, "sO", &msg, &obj) &&
               !strcmp (msg, "unexpected EOF while parsing")) /* E_EOF */
           {
             Py_XDECREF (exc);
             Py_XDECREF (val);
             Py_XDECREF (trb);
             prompt = ps2;
           }
           else                                   /* some other syntax error */
           {
             PyErr_Restore (exc, val, trb);
             PyErr_Print ();
             free (code);
             code = NULL;
             prompt = ps1;
           }
         }
         else                                     /* some non-syntax error */
         {
           PyErr_Print ();
           free (code);
           code = NULL;
           prompt = ps1;
         }

         free (line);
       }
     }

     Py_XDECREF(glb);
     Py_XDECREF(loc);
     Py_Finalize();
     exit(0);
   }


如何找到未定义的g++符号__builtin_new或__pure_virtual？
======================================================

要动态加载g ++扩展模块，必须重新编译Python，要使用g ++重新链接（在
Python Modules Makefile中更改LINKCC），及链接扩展模块（例如： "g++
-shared -o mymodule.so mymodule.o" ）。


能否创建一个对象类，其中部分方法在C中实现，而其他方法在Python中实现（例如通过继承）？
=====================================================================================

是的，您可以继承内置类，例如 "int" ， "list" ， "dict" 等。

Boost Python库（BPL，http：//www.boost.org/libs/python/doc/index.html
）提供了一种从C ++执行此操作的方法（即，您可以使用BPL继承自C ++编写的
扩展类 ）。
