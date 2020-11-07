字节数组对象
************

PyByteArrayObject

   这个 "PyObject" 的子类型表示一个 Python 字节数组对象。

PyTypeObject PyByteArray_Type

   Python bytearray 类型表示为 "PyTypeObject" 的实例；这与Python层面的
   "bytearray" 是相同的对象。


类型检查宏
==========

int PyByteArray_Check(PyObject *o)

   当对象 *o* 是一个字节数组对象而且是一个字节数组类型的子类型实例时，
   返回真。

int PyByteArray_CheckExact(PyObject *o)

   当对象 *o* 是一个字节数组对象，但不是一个字节数组类型的子类型实例时
   ，返回真。


直接 API 函数
=============

PyObject* PyByteArray_FromObject(PyObject *o)
    *Return value: New reference.*

   根据任何实现了 缓冲区协议 的对象 *o*，返回一个新的字节数组对象。

PyObject* PyByteArray_FromStringAndSize(const char *string, Py_ssize_t len)
    *Return value: New reference.*

   根据 *string* 及其长度 *len* 创建一个新的 bytearray 对象。 当失败时
   返回 "NULL"。

PyObject* PyByteArray_Concat(PyObject *a, PyObject *b)
    *Return value: New reference.*

   连接字节数组 *a* 和 *b* 并返回一个带有结果的新的字节数组。

Py_ssize_t PyByteArray_Size(PyObject *bytearray)

   在检查 "NULL" 指针后返回 *bytearray* 的大小。

char* PyByteArray_AsString(PyObject *bytearray)

   在检查 "NULL" 指针后返回将 *bytearray* 返回为一个字符数组。 返回的
   数组总是会附加一个额外的空字节。

int PyByteArray_Resize(PyObject *bytearray, Py_ssize_t len)

   将 *bytearray* 的内部缓冲区的大小调整为 *len*。


宏
==

这些宏减低安全性以换取性能，它们不检查指针。

char* PyByteArray_AS_STRING(PyObject *bytearray)

   C函数 "PyByteArray_AsString()" 的宏版本。

Py_ssize_t PyByteArray_GET_SIZE(PyObject *bytearray)

   C函数 "PyByteArray_Size()" 的宏版本。
