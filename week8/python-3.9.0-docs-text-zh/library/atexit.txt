"atexit" --- 退出处理器
***********************

======================================================================

"atexit" 模块定义了清理函数的注册和反注册函数. 被注册的函数会在解释器
正常终止时执行. "atexit" 会按照注册顺序的*逆序*执行; 如果你注册了 "A",
"B" 和 "C", 那么在解释器终止时会依序执行 "C", "B", "A".

**注意:** 通过该模块注册的函数, 在程序被未被 Python 捕获的信号杀死时并
不会执行, 在检测到 Python 内部致命错误以及调用了 "os._exit()" 时也不会
执行.

在 3.7 版更改: 当配合 C-API 子解释器使用时，已注册函数是它们所注册解释
器中的局部对象。

atexit.register(func, *args, **kwargs)

   将 *func* 注册为终止时执行的函数.  任何传给 *func* 的可选的参数都应
   当作为参数传给 "register()".  可以多次注册同样的函数及参数.

   在正常的程序终止时 (举例来说, 当调用了 "sys.exit()" 或是主模块的执
   行完成时), 所有注册过的函数都会以后进先出的顺序执行. 这样做是假定更
   底层的模块通常会比高层模块更早引入, 因此需要更晚清理.

   如果在 exit 处理程序执行期间引发了异常，将会打印回溯信息 (除非引发
   的是 "SystemExit") 并且异常信息会被保存。 在所有 exit 处理程序获得
   运行机会之后，所引发的最后一个异常会被重新引发。

   这个函数返回 *func* 对象，可以把它当作装饰器使用。

atexit.unregister(func)

   从解释器关闭前要运行的函数列表中移除 *func*。 在调用 "unregister()"
   之后，当解释器关闭时会确保 *func* 不会被调用，即使它被多次注册。 如
   果 *func* 之前没有被注册，"unregister()" 会静默地不做任何操作。

参见:

  模块 "readline"
     使用 "atexit" 读写 "readline" 历史文件的有用的例子。


"atexit" 示例
=============

以下简单例子演示了一个模块在被导入时如何从文件初始化一个计数器，并在程
序终结时自动保存计数器的更新值，此操作不依赖于应用在终结时对此模块进行
显式调用。:

   try:
       with open("counterfile") as infile:
           _count = int(infile.read())
   except FileNotFoundError:
       _count = 0

   def incrcounter(n):
       global _count
       _count = _count + n

   def savecounter():
       with open("counterfile", "w") as outfile:
           outfile.write("%d" % _count)

   import atexit
   atexit.register(savecounter)

位置和关键字参数也可传入 "register()" 以便传递给被调用的已注册函数:

   def goodbye(name, adjective):
       print('Goodbye, %s, it was %s to meet you.' % (name, adjective))

   import atexit
   atexit.register(goodbye, 'Donny', 'nice')

   # or:
   atexit.register(goodbye, adjective='nice', name='Donny')

作为 *decorator*: 使用:

   import atexit

   @atexit.register
   def goodbye():
       print("You are now leaving the Python sector.")

只有在函数不需要任何参数调用时才能工作.
