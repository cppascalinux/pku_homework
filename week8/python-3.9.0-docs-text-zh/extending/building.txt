4. 构建C/C++扩展
****************

一个CPython的C扩展是一个共享库(例如一个Linux上的 ".so" ，或者Windows上
的 ".pyd" )，其会导出一个 *初始化函数* 。

为了可导入，共享库必须在 "PYTHONPATH" 中有效，且必须命名遵循模块名字，
通过适当的扩展。当使用distutils时，会自动生成正确的文件名。

初始化函数的声明如下：

PyObject* PyInit_modulename(void)

该函数返回完整初始化过的模块，或一个 "PyModuleDef" 实例。查看
Initializing C modules 了解更多细节。

对于仅有ASCII编码的模块名，函数必须是 "PyInit_<modulename>" ，将
"<modulename>" 替换为模块的名字。当使用 Multi-phase initialization 时
，允许使用非ASCII编码的模块名。此时初始化函数的名字是
"PyInitU_<modulename>" ，而 "<modulename>" 需要用Python的 *punycode*
编码，连字号需替换为下划线。在Python里:

   def initfunc_name(name):
       try:
           suffix = b'_' + name.encode('ascii')
       except UnicodeEncodeError:
           suffix = b'U_' + name.encode('punycode').replace(b'-', b'_')
       return b'PyInit' + suffix

可以在一个动态库里导出多个模块，通过定义多个初始化函数。而导入他们需要
符号链接或自定义导入器，因为缺省时只有对应了文件名的函数才会被发现。查
看 *"一个库里的多模块"* 章节，在 **PEP 489** 了解更多细节。


4.1. 使用distutils构建C和C++扩展
================================

扩展模块可以用distutils来构建，这是Python自带的。distutils也支持创建二
进制包，用户无需编译器而distutils就能安装扩展。

一个distutils包包含了一个驱动脚本 "setup.py" 。这是个纯Python文件，大
多数时候也很简单，看起来如下：

   from distutils.core import setup, Extension

   module1 = Extension('demo',
                       sources = ['demo.c'])

   setup (name = 'PackageName',
          version = '1.0',
          description = 'This is a demo package',
          ext_modules = [module1])

通过文件 "setup.py" ，和文件 "demo.c" ，运行如下

   python setup.py build

这会编译 "demo.c" ，然后产生一个扩展模块叫做 "demo" 在目录 "build" 里
。依赖于系统，模块文件会放在某个子目录形如 "build/lib.system" ，名字可
能是 "demo.so" 或 "demo.pyd" 。

在文件 "setup.py" 里，所有动作的入口通过 "setup" 函数。该函数可以接受
可变数量个关键字参数，上面的例子只使用了一个子集。特别需要注意的例子指
定了构建包的元信息，以及指定了包内容。通常一个包会包括多个模块，就像
Python的源码模块、文档、子包等。请参数distutils的文档，在 分发 Python
模块（遗留版本） 来了解更多distutils的特性；本章节只解释构建扩展模块的
部分。

通常预计算参数给 "setup()" ，想要更好的结构化驱动脚本。有如如上例子函
数 "setup()" 的 "ext_modules" 参数是一列扩展模块，每个是一个
"Extension" 类的实例。例子中的实例定义了扩展命名为 "demo" ，从单一源码
文件构建 "demo.c" 。

更多时候，构建一个扩展会复杂的多，需要额外的预处理器定义和库。如下例子
展示了这些。

   from distutils.core import setup, Extension

   module1 = Extension('demo',
                       define_macros = [('MAJOR_VERSION', '1'),
                                        ('MINOR_VERSION', '0')],
                       include_dirs = ['/usr/local/include'],
                       libraries = ['tcl83'],
                       library_dirs = ['/usr/local/lib'],
                       sources = ['demo.c'])

   setup (name = 'PackageName',
          version = '1.0',
          description = 'This is a demo package',
          author = 'Martin v. Loewis',
          author_email = 'martin@v.loewis.de',
          url = 'https://docs.python.org/extending/building',
          long_description = '''
   This is really just a demo package.
   ''',
          ext_modules = [module1])

例子中函数 "setup()" 在调用时额外传递了元信息，是推荐发布包构建时的内
容。对于这个扩展，其指定了预处理器定义，include目录，库目录，库。依赖
于编译器，distutils还会用其他方式传递信息给编译器。例如在Unix上，结果
是如下编译命令

   gcc -DNDEBUG -g -O3 -Wall -Wstrict-prototypes -fPIC -DMAJOR_VERSION=1 -DMINOR_VERSION=0 -I/usr/local/include -I/usr/local/include/python2.2 -c demo.c -o build/temp.linux-i686-2.2/demo.o

   gcc -shared build/temp.linux-i686-2.2/demo.o -L/usr/local/lib -ltcl83 -o build/lib.linux-i686-2.2/demo.so

这些行代码仅用于展示目的；distutils用户应该相信distutils能正确调用。


4.2. 发布你的扩展模块
=====================

当一个扩展已经成功地被构建时，有三种方式来使用它。

最终用户通常想要安装模块，可以这么运行

   python setup.py install

模块维护者应该制作源码包；要实现可以运行

   python setup.py sdist

有些情况下，需要在源码发布包里包含额外的文件；这通过 "MANIFEST.in" 文
件实现，查看 Specifying the files to distribute 了解细节。

如果源码发行包被成功地构建，维护者还可以创建二进制发行包。 取决于具体
平台，以下命令中的一个可以用来完成此任务

   python setup.py bdist_wininst
   python setup.py bdist_rpm
   python setup.py bdist_dumb
