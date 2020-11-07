迭代器对象
**********

Python 提供了两个通用迭代器对象。 第一个是序列迭代器，它使用支持
"__getitem__()" 方法的任意序列。 第二个使用可调用对象和一个 sentinel
值，为序列中的每个项调用可调用对象，并在返回 sentinel 值时结束迭代。

PyTypeObject PySeqIter_Type

   "PySeqIter_New()" 返回迭代器对象的类型对象和内置序列类型内置函数
   "iter()" 的单参数形式。

int PySeqIter_Check(op)

   如果 *op* 的类型为 "PySeqIter_Type" 则返回 true。

PyObject* PySeqIter_New(PyObject *seq)
    *Return value: New reference.*

   返回一个与常规序列对象一起使用的迭代器 *seq*。 当序列订阅操作引发
   "IndexError" 时，迭代结束。

PyTypeObject PyCallIter_Type

   由函数 "PyCallIter_New()" 和 "iter()" 内置函数的双参数形式返回的迭
   代器对象类型对象。

int PyCallIter_Check(op)

   如果 *op* 的类型为 "PyCallIter_Type" 则返回 true。

PyObject* PyCallIter_New(PyObject *callable, PyObject *sentinel)
    *Return value: New reference.*

   返回一个新的迭代器。 第一个参数 *callable* 可以是任何可以在没有参数
   的情况下调用的 Python 可调用对象；每次调用都应该返回迭代中的下一个
   项目。 当 *callable* 返回等于 *sentinel* 的值时，迭代将终止。
