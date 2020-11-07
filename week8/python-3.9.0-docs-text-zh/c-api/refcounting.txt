引用计数
********

本节介绍的宏被用于管理 Python 对象的引用计数。

void Py_INCREF(PyObject *o)

   增加对象 *o* 的引用计数。 对象必须不为 "NULL"；如果你不确定它不为
   "NULL"，可使用 "Py_XINCREF()"。

void Py_XINCREF(PyObject *o)

   增加对象 *o* 的引用计数。 对象可以为 "NULL"，在此情况下该宏不产生任
   何效果。

void Py_DECREF(PyObject *o)

   减少对象 *o* 的引用计数。 对象必须不为 "NULL"；如果你不确定它不为
   "NULL"，可使用 "Py_XDECREF()"。 如果引用计数降为零，将发起调用对象
   所属类型的释放函数 (它必须不为 "NULL")。

   警告:

     释放函数可导致任意 Python 代码被发起调用（例如当一个带有
     "__del__()" 方法的类实例被释放时就是如此）。 虽然此类代码中的异常
     不会被传播，但被执行的代码能够自由访问所有 Python 全局变量。 这意
     味着任何可通过全局变量获取的对象在  "Py_DECREF()" 被发起调用之前
     都应当处于完好状态。 例如，从一个列表中删除对象的代码应当将被删除
     对象的引用拷贝到一个临时变量中，更新列表数据结构，然后再为临时变
     量调用 "Py_DECREF()"。

void Py_XDECREF(PyObject *o)

   减少对象 *o* 的引用计数。 对象可以为 "NULL"，在此情况下该宏不产生任
   何效果；在其他情况下其效果与 "Py_DECREF()" 相同，并会应用同样的警告
   。

void Py_CLEAR(PyObject *o)

   减少对象 *o* 的引用计数。 对象可以为 "NULL"，在此情况下该宏不产生任
   何效果；在其他情况下其效果与 "Py_DECREF()" 相同，区别在于其参数也会
   被设为 "NULL"。 针对 "Py_DECREF()" 的警告不适用于所传递的对象，因为
   该宏会细心地使用一个临时变量并在减少其引用计数之前将参数设为 "NULL"
   。

   每当要减少在垃圾回收期间可能会被遍历的对象的引用计数时，使用该宏是
   一个好主意。

以下函数适用于 Python 的运行时动态嵌入: "Py_IncRef(PyObject *o)",
"Py_DecRef(PyObject *o)"。 它们分别只是 "Py_XINCREF()" 和
"Py_XDECREF()" 的简单导出函数版本。

以下函数或宏仅可在解释器核心内部使用: "_Py_Dealloc()",
"_Py_ForgetReference()", "_Py_NewReference()" 以及全局变量
"_Py_RefTotal"。
