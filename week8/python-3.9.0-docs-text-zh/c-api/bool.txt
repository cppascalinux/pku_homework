布尔对象
********

Python 中的布尔值是作为整数的子类实现的。只有 "Py_False" 和 "Py_True"
两个布尔值。因此，正常的创建和删除功能不适用于布尔值。但是，下列宏可用
。

int PyBool_Check(PyObject *o)

   如果  *o*  的类型为 "PyBool_Type"，则返回 true。

PyObject* Py_False

   Python 的  "False" 对象没有任何方法，它需要和其他对象一样遵循引用计
   数。

PyObject* Py_True

   Python 的 "True" 对象没有任何方法，它需要和其他对象一样遵循引用计数
   。

Py_RETURN_FALSE

   从函数返回 "Py_False" 时，需要增加它的引用计数。

Py_RETURN_TRUE

   从函数返回 "Py_True" 时，需要增加它的引用计数。

PyObject* PyBool_FromLong(long v)
    *Return value: New reference.*

   根据 *v* 的实际值，返回一个 "Py_True" 或者 "Py_False" 的新引用。
